import os
import tempfile
import pytest

import usuario
import principal
import vagas
import estacionamento
import fila

import builtins
import io
import sys
import types
import csv
import importlib


from unittest.mock import patch, MagicMock

# ======================== Globais =============================
FILA = None
ESTACIONAMENTOS = []
USUARIO_ATUAL = None

# ======================== Testes =============================

def teste_login_com_sucesso():
    """Testa carregamento de usuários de CSV"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("user123,senha123,1\n")
        temp_file = f.name
    try:
        usuario.carregarUsuarios(temp_file)
        assert usuario.autentica("user123", "senha123") == {'login': 'user123', 'senha': 'senha123', 'tipo': 1}
    finally:
        os.unlink(temp_file)

def teste_login_com_falha():
    """Testa carregamento de usuários com senha incorreta"""
    usuario.usuarios.clear()
    usuario.convidados.clear()
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("user123,senha123,1\n")
        temp_file = f.name
    try:
        usuario.carregarUsuarios(temp_file)
        assert usuario.autentica("user123", "senha235") == 2
    finally:
        os.unlink(temp_file)

# -----------------------------------------------
# Testes para IniciarSistema
# -----------------------------------------------
@patch("usuario.carregarUsuarios")
@patch("estacionamento.criar_estacionamentos_de_csv", return_value=["Est1", "Est2"])
def test_iniciar_sistema(mock_criar_estacionamentos, mock_carregar_usuarios):
    principal.IniciarSistema()
    mock_carregar_usuarios.assert_any_call("users.csv")
    mock_carregar_usuarios.assert_any_call("guests.csv", tipo_padrao=2)
    mock_criar_estacionamentos.assert_called_once_with("estacionamentos.csv")
    assert principal.ESTACIONAMENTOS == ["Est1", "Est2"]

# -----------------------------------------------
# Testes para MenuInicial
# -----------------------------------------------
@patch("builtins.input", side_effect=["3"])
@patch("principal.EncerrarSistema", side_effect=SystemExit)
def test_menu_inicial_sair(mock_encerrar, mock_input):
    with pytest.raises(SystemExit):
        principal.MenuInicial()
    mock_encerrar.assert_called_once()

@patch("builtins.input", side_effect=["1", "login", "senha", "3"])
@patch("principal.AutenticarUsuario")
@patch("principal.EncerrarSistema", side_effect=SystemExit)
def test_menu_inicial_login(mock_encerrar, mock_autenticar, mock_input):
    mock_autenticar.return_value = {"login": "teste"}
    with pytest.raises(SystemExit):
        principal.MenuInicial()
    mock_autenticar.assert_called()

# -----------------------------------------------
# Testes para TratarErros
# -----------------------------------------------
@patch("builtins.print")
def test_tratar_erros_known_code(mock_print):
    principal.TratarErros("OPCAO_INVALIDA")
    mock_print.assert_called_once_with("⚠️  Opção inválida!")

@patch("builtins.print")
def test_tratar_erros_unknown_code(mock_print):
    principal.TratarErros("ERRO_DESCONHECIDO")
    mock_print.assert_called_once_with("⚠️  Erro desconhecido.")

# -----------------------------------------------
# Testes para AlocarVaga
# -----------------------------------------------
@patch("estacionamento.selecionar_estacionamento")
@patch("estacionamento.get_vaga_disponivel")
@patch("estacionamento.ocupar_vaga_por_login")
@patch("builtins.print")
def test_alocar_vaga_sucesso(mock_print, mock_ocupar, mock_get_vaga, mock_selecionar):
    principal.USUARIO_ATUAL = {"login": "teste"}
    mock_selecionar.return_value = "est"
    mock_get_vaga.return_value = {"id": 42}
    mock_ocupar.return_value = (True, 42)
    principal.AlocarVaga()
    mock_print.assert_any_call("✅ Vaga 42 ocupada. Boa estadia!")

@patch("estacionamento.selecionar_estacionamento")
@patch("estacionamento.get_vaga_disponivel")
@patch("principal.GerenciaFila")
@patch("principal.TratarErros")
def test_alocar_vaga_sem_vaga(mock_tratar, mock_gerencia, mock_get_vaga, mock_selecionar):
    principal.USUARIO_ATUAL = {"login": "teste"}
    mock_selecionar.return_value = "est"
    mock_get_vaga.return_value = None
    principal.AlocarVaga()
    mock_gerencia.assert_called_once()
    mock_tratar.assert_called_with("SEM_VAGAS")

@patch("principal.TratarErros")
def test_alocar_vaga_sem_autenticacao(mock_tratar):
    principal.USUARIO_ATUAL = None
    principal.AlocarVaga()
    mock_tratar.assert_called_with("NAO_AUTENTICADO")

# -----------------------------------------------
# Testes para LiberarVaga
# -----------------------------------------------
@patch("estacionamento.liberar_vaga_de", return_value=99)
@patch("estacionamento.getNome", return_value="Est1")
@patch("principal.AtualizarEstado")
@patch("builtins.print")
def test_liberar_vaga_sucesso(mock_print, mock_atualizar, mock_getnome, mock_liberar):
    principal.USUARIO_ATUAL = {"login": "teste"}
    principal.ESTACIONAMENTOS = ["est"]
    principal.LiberarVaga()
    mock_print.assert_any_call("✅ Vaga 99 liberada no estacionamento 'Est1'.")
    mock_atualizar.assert_called_once()

@patch("estacionamento.liberar_vaga_de", return_value=None)
@patch("principal.TratarErros")
def test_liberar_vaga_nao_encontrada(mock_tratar, mock_liberar):
    principal.USUARIO_ATUAL = {"login": "teste"}
    principal.ESTACIONAMENTOS = ["est"]
    principal.LiberarVaga()
    mock_tratar.assert_called_with("VAGA_NAO_ENCONTRADA")

# -----------------------------------------------
# Testes para ExibirResumo
# -----------------------------------------------
@patch("estacionamento.listar_estacionamentos")
@patch("fila.tamanhoFila", return_value=5)
@patch("builtins.print")
def test_exibir_resumo_autenticado(mock_print, mock_tamanho, mock_listar):
    principal.USUARIO_ATUAL = {"login": "user"}
    principal.ExibirResumo()
    mock_listar.assert_called_once_with(principal.ESTACIONAMENTOS)
    mock_tamanho.assert_called_once()
    mock_print.assert_any_call("Usuário autenticado: user")

@patch("estacionamento.listar_estacionamentos")
@patch("fila.tamanhoFila", return_value=0)
@patch("builtins.print")
def test_exibir_resumo_sem_autenticado(mock_print, mock_tamanho, mock_listar):
    principal.USUARIO_ATUAL = None
    principal.ExibirResumo()
    mock_print.assert_any_call("Nenhum usuário autenticado.")

# -----------------------------------------------
# Teste para EncerrarSistema
# -----------------------------------------------
@patch("usuario.salvarUsuarios")
@patch("estacionamento.salvar_estado_em_csv")
@patch("builtins.open")
@patch("csv.writer")
@patch("builtins.print")
def test_encerrar_sistema(mock_print, mock_writer, mock_open, mock_salvar_estado, mock_salvar_usuarios):
    mock_open.return_value.__enter__.return_value = MagicMock()
    with pytest.raises(SystemExit):
        principal.EncerrarSistema()
    mock_salvar_usuarios.assert_called_once()
    mock_print.assert_any_call("✔️  Dados salvos. Até logo!")

#------------------------------------------------------------------------------------------------------------------------

@patch("builtins.input", side_effect=["1", "login", "senha", "99", "3"])
@patch("principal.TratarErros")
@patch("principal.AutenticarUsuario", return_value={"login": "user"})
@patch("principal.EncerrarSistema", side_effect=SystemExit)
def test_menu_inicial_opcao_invalida(mock_encerrar, mock_autenticar, mock_tratar, mock_input):
    with pytest.raises(SystemExit):
        principal.MenuInicial()
    mock_tratar.assert_called_with("OPCAO_INVALIDA")





# ---------------------------------------------------------------------------
# Fixtures utilitárias
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _reset_globais(monkeypatch):
    """Restaura variáveis globais a cada teste para evitar interferência."""
    principal.ESTACIONAMENTOS = []
    principal.USUARIO_ATUAL = None
    yield
    principal.ESTACIONAMENTOS = []
    principal.USUARIO_ATUAL = None


# ---------------------------------------------------------------------------
# AutenticarUsuario
# ---------------------------------------------------------------------------

def test_autenticar_usuario_sucesso(monkeypatch, capsys):
    entradas = iter(["john", "secret"])
    monkeypatch.setattr(builtins, "input", lambda _: next(entradas))

    user_obj = {"login": "john"}
    monkeypatch.setattr(principal.usuario_mod, "autentica", lambda l, s: user_obj)
    monkeypatch.setattr(principal.usuario_mod, "getLogin", lambda u: u["login"])

    principal.AutenticarUsuario()
    out = capsys.readouterr().out

    assert "Bem-vindo" in out
    assert principal.USUARIO_ATUAL == user_obj


def test_autenticar_usuario_login_inexistente(monkeypatch, capsys):
    entradas = iter(["john", "secret"])
    monkeypatch.setattr(builtins, "input", lambda _: next(entradas))

    monkeypatch.setattr(principal.usuario_mod, "autentica", lambda l, s: 1)

    principal.AutenticarUsuario()
    out = capsys.readouterr().out

    assert "Login inexistente" in out
    assert principal.USUARIO_ATUAL is None




