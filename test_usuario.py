import pytest
import tempfile
import os
import usuario
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Testes para funções da interface pública do módulo usuario
# ---------------------------------------------------------------------------

def teste_get_login():
    """Testa função de acesso ao login"""
    user = usuario.novo_usuario("1234567", "senha", 1)
    assert usuario.getLogin(user) == "1234567"

def teste_get_tipo_interno():
    """Testa função de acesso ao tipo - usuário interno"""
    user1 = usuario.novo_usuario("1234567", "senha", 1)
    assert usuario.getTipo(user1) == 1

def teste_get_tipo_convidado():
    """Testa função de acesso ao tipo - usuário convidado"""
    user2 = usuario.novo_usuario("1234568", "senha", 2)
    assert usuario.getTipo(user2) == 2

def teste_get_tipo_erro():
    """Testa função de acesso ao tipo - caso de erro"""
    assert usuario.getTipo(None) == -1

def teste_autentica_sucesso():
    """Testa autenticação com sucesso"""
    usuario.usuarios.clear()
    user = usuario.novo_usuario("1234567", "senha123", 1)
    usuario.usuarios.append(user)
    
    resultado = usuario.autentica("1234567", "senha123")
    assert resultado == user

def teste_autentica_login_inexistente():
    """Testa autenticação com login inexistente"""
    usuario.usuarios.clear()
    resultado = usuario.autentica("9999999", "abc123")
    assert resultado == 1

def teste_autentica_senha_incorreta():
    """Testa autenticação com senha incorreta"""
    usuario.usuarios.clear()
    usuario.usuarios.append(usuario.novo_usuario("2311213", "abc123", 1))
    resultado = usuario.autentica("2311213", "jjj567")
    assert resultado == 2

def teste_autentica_campos_invalidos():
    """Testa autenticação com campos inválidos"""
    resultado = usuario.autentica("", "")
    assert resultado == 3

def teste_autentica_convidado():
    """Testa autenticação de convidado"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    convidado = usuario.novo_usuario("11122233344", "guest123", 2)
    usuario.usuarios.append(convidado)
    usuario.convidados.append(convidado)
    
    resultado = usuario.autentica("11122233344", "guest123")
    assert isinstance(resultado, dict)
    assert usuario.getLogin(resultado) == "11122233344"

def teste_carregar_usuarios():
    """Testa carregamento de usuários de CSV"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("1234567,senha123,1\n")
        f.write("11122233344,guest123,2\n")
        temp_file = f.name
    
    try:
        usuario.carregarUsuarios(temp_file)
        
        assert len(usuario.usuarios) == 2
        user1 = usuario.buscarUsuario("1234567")
        user2 = usuario.buscarUsuario("11122233344")
        
        assert user1 is not None
        assert usuario.getTipo(user1) == 1
        assert user2 is not None
        assert usuario.getTipo(user2) == 2
        assert len(usuario.convidados) == 1
    finally:
        os.unlink(temp_file)

def teste_salvar_usuarios():
    """Testa salvamento de usuários em CSV"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    
    # Adiciona usuários
    usuario.usuarios.append(usuario.novo_usuario("1234567", "senha123", 1))
    convidado = usuario.novo_usuario("11122233344", "guest123", 2)
    usuario.usuarios.append(convidado)
    usuario.convidados.append(convidado)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        users_file = os.path.join(temp_dir, "users.csv")
        guests_file = os.path.join(temp_dir, "guests.csv")
        
        usuario.salvarUsuarios(users_file, guests_file)
        
        # Verifica se arquivos foram criados
        assert os.path.exists(users_file)
        assert os.path.exists(guests_file)
        
        # Verifica conteúdo
        with open(users_file, 'r') as f:
            content = f.read()
            assert "1234567,senha123,1" in content
        
        with open(guests_file, 'r') as f:
            content = f.read()
            assert "11122233344,guest123,2" in content

# ---------------------------------------------------------------------------
# Testes para funções interativas usando mock
# ---------------------------------------------------------------------------

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_interno_sucesso(mock_print, mock_input):
    """Testa criação bem-sucedida de usuário interno"""
    usuario.usuarios.clear()
    mock_input.side_effect = ["1234567", "minhasenha"]
    
    usuario.criaInterno()
    
    assert len(usuario.usuarios) == 1
    user = usuario.usuarios[0]
    assert usuario.getLogin(user) == "1234567"
    assert user["senha"] == "minhasenha"
    assert usuario.getTipo(user) == 1

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_interno_matricula_invalida_depois_valida(mock_print, mock_input):
    """Testa criação com matrícula inválida primeiro, depois válida"""
    usuario.usuarios.clear()
    mock_input.side_effect = ["123456", "12345678", "123abc7", "1234567", "senha123"]
    
    usuario.criaInterno()
    
    assert len(usuario.usuarios) == 1
    assert usuario.getLogin(usuario.usuarios[0]) == "1234567"

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_interno_matricula_existente(mock_print, mock_input):
    """Testa tentativa de criação com matrícula já existente"""
    usuario.usuarios.clear()
    usuario.usuarios.append(usuario.novo_usuario("1234567", "senha", 1))
    mock_input.side_effect = ["1234567", "7654321", "novasenha"]
    
    usuario.criaInterno()
    
    assert len(usuario.usuarios) == 2
    user_novo = next(u for u in usuario.usuarios if usuario.getLogin(u) == "7654321")
    assert user_novo["senha"] == "novasenha"

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_interno_cancelamento(mock_print, mock_input):
    """Testa cancelamento da criação de usuário interno"""
    usuario.usuarios.clear()
    inicial_count = len(usuario.usuarios)
    mock_input.side_effect = ["0"]
    
    usuario.criaInterno()
    
    assert len(usuario.usuarios) == inicial_count

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_interno_senha_vazia(mock_print, mock_input):
    """Testa criação com senha vazia"""
    usuario.usuarios.clear()
    mock_input.side_effect = ["1234567", ""]
    
    usuario.criaInterno()
    
    assert len(usuario.usuarios) == 0

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_convidado_sucesso(mock_print, mock_input):
    """Testa criação bem-sucedida de usuário convidado"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    # Adiciona CPF autorizado na lista de convidados
    usuario.convidados.append(usuario.novo_usuario("11122233344", "temp", 2))
    mock_input.side_effect = ["11122233344", "senhaconvidado"]
    
    usuario.criaConvidado()
    
    # Verifica se foi adicionado aos usuários (além de já estar em convidados)
    user = usuario.buscarUsuario("11122233344")
    assert user is not None
    assert user["senha"] == "senhaconvidado"
    assert usuario.getTipo(user) == 2

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_convidado_cpf_invalido_depois_valido(mock_print, mock_input):
    """Testa criação com CPF inválido primeiro, depois válido"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    usuario.convidados.append(usuario.novo_usuario("11122233344", "temp", 2))
    mock_input.side_effect = ["1112223334", "111222333445", "11a22233344", "11122233344", "senha123"]
    
    usuario.criaConvidado()
    
    user = usuario.buscarUsuario("11122233344")
    assert user is not None
    assert user["senha"] == "senha123"

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_convidado_cpf_nao_autorizado(mock_print, mock_input):
    """Testa tentativa com CPF não autorizado"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    # Lista de convidados vazia - CPF não autorizado
    mock_input.side_effect = ["11122233344", "0"]
    
    usuario.criaConvidado()
    
    user = usuario.buscarUsuario("11122233344")
    assert user is None

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_convidado_cpf_ja_convidado(mock_print, mock_input):
    """Testa CPF que já recebeu acesso de convidado"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    # CPF já existe como usuário convidado
    convidado_existente = usuario.novo_usuario("11122233344", "senhaantiga", 2)
    usuario.usuarios.append(convidado_existente)
    usuario.convidados.append(convidado_existente)
    mock_input.side_effect = ["11122233344"]
    
    usuario.criaConvidado()
    
    # Deve manter apenas o usuário original
    users_com_cpf = [u for u in usuario.usuarios if usuario.getLogin(u) == "11122233344"]
    assert len(users_com_cpf) == 1
    assert users_com_cpf[0]["senha"] == "senhaantiga"

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_convidado_cancelamento(mock_print, mock_input):
    """Testa cancelamento da criação de convidado"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    inicial_count = len(usuario.usuarios)
    mock_input.side_effect = ["0"]
    
    usuario.criaConvidado()
    
    assert len(usuario.usuarios) == inicial_count

@patch('builtins.input')
@patch('builtins.print')
def teste_cria_convidado_senha_vazia(mock_print, mock_input):
    """Testa criação de convidado com senha vazia"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    usuario.convidados.append(usuario.novo_usuario("11122233344", "temp", 2))
    mock_input.side_effect = ["11122233344", ""]
    
    inicial_count = len(usuario.usuarios)
    usuario.criaConvidado()
    
    # Não deve adicionar usuário se senha for vazia
    assert len(usuario.usuarios) == inicial_count

def test_validaLogin_ok():
    assert usuario.validaLogin("1234567") is True

def test_validaLogin_tamanho_errado():
    # 6 e 8 dígitos → False
    assert usuario.validaLogin("123456") is False
    assert usuario.validaLogin("12345678") is False

def test_validaLogin_nao_numerico():
    # contém letra
    assert usuario.validaLogin("1234a67") is False

def test_loginExiste_true_false():
    usuario.usuarios.clear()
    usuario.usuarios.append(usuario.novo_usuario("7654321", "x", 1))

    assert usuario.loginExiste("7654321") is True   # já existe
    assert usuario.loginExiste("9999999") is False  # não existe

def test_cpfConvidadoValido_true_false():
    usuario.convidados.clear()
    usuario.convidados.append(usuario.novo_usuario("11122233344", "x", 2))

    assert usuario.cpfConvidadoValido("11122233344") is True   # presente
    assert usuario.cpfConvidadoValido("55566677788") is False  # ausente