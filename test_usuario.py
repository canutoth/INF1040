import pytest
import tempfile
import os
import usuario

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

def teste_get_tipo_externo():
    """Testa função de acesso ao tipo - usuário externo"""
    user3 = usuario.novo_usuario("1234569", "senha", 3)
    assert usuario.getTipo(user3) == 3

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
    resultado = usuario.autentica("", " ")
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

# Nota: criaInterno() e criaConvidado() não são testadas diretamente pois 
# dependem de input/output do usuário. Suas funcionalidades são testadas 
# indiretamente através dos testes de autentica(), carregarUsuarios() e salvarUsuarios().
