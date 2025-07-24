import os
import pytest
import fila
from fila import (
    consultarPosicaoNaFila,
    adicionarNaFila,
    removerDaFila,
    ordenarFilaPorPrioridade,
    retornaPrimeiro,
    tamanhoFila,
    carregar_fila_de_csv,
    salvar_fila_em_csv,
)

# Fixture para limpar a fila antes de cada teste
@pytest.fixture(autouse=True)
def _reset_fila():
    fila._FILA.clear()
    yield
    fila._FILA.clear()

def teste_fila_inicialmente_vazia():
    assert tamanhoFila() == 0

def teste_consultar_fila_vazia():
    assert consultarPosicaoNaFila("U1") == -1

def teste_adicionar_na_fila_vazia():
    usuario = {"login": "U1", "tipo": 1}
    ret = adicionarNaFila(usuario)
    assert ret == 0
    assert tamanhoFila() == 1
    assert consultarPosicaoNaFila("U1") == 1

def teste_consultar_em_fila_com_um_elemento():
    usuario = {"login": "U1", "tipo": 1}
    adicionarNaFila(usuario)
    assert consultarPosicaoNaFila("U1") == 1

def teste_consultar_usuario_inexistente():
    usuario = {"login": "U1", "tipo": 1}
    adicionarNaFila(usuario)
    assert consultarPosicaoNaFila("U9") == -1

def teste_rejeicao_de_duplicata():
    usuario = {"login": "U1", "tipo": 1}
    ret1 = adicionarNaFila(usuario)
    ret2 = adicionarNaFila(usuario)
    assert ret1 == 0
    assert ret2 == -1
    assert tamanhoFila() == 1

def teste_ordenacao_por_prioridade():
    usuario1 = {"login": "U1", "tipo": 3}
    usuario2 = {"login": "U2", "tipo": 2}
    usuario3 = {"login": "U3", "tipo": 1}
    
    adicionarNaFila(usuario1)
    adicionarNaFila(usuario2)
    adicionarNaFila(usuario3)
    
    # Verifica se estão ordenados por prioridade
    assert consultarPosicaoNaFila("U3") == 1  # tipo 1 primeiro
    assert consultarPosicaoNaFila("U2") == 2  # tipo 2 segundo
    assert consultarPosicaoNaFila("U1") == 3  # tipo 3 terceiro

def teste_preservacao_ordem_mesma_prioridade():
    usuario1 = {"login": "U1", "tipo": 2}  # chegou antes
    usuario2 = {"login": "U2", "tipo": 2}
    
    adicionarNaFila(usuario1)
    adicionarNaFila(usuario2)
    
    # U1 deve estar antes de U2 (mesma prioridade, mas chegou primeiro)
    assert consultarPosicaoNaFila("U1") == 1
    assert consultarPosicaoNaFila("U2") == 2

def teste_ordenacao_idempotente_em_fila_vazia():
    ordenarFilaPorPrioridade()
    assert tamanhoFila() == 0

def teste_ordenacao_idempotente_em_fila_um_elemento():
    usuario = {"login": "U1", "tipo": 1}
    adicionarNaFila(usuario)
    ordenarFilaPorPrioridade()
    assert consultarPosicaoNaFila("U1") == 1
    assert tamanhoFila() == 1

def teste_remocao_usuario_inexistente():
    usuario1 = {"login": "U1", "tipo": 1}
    usuario2 = {"login": "U2", "tipo": 2}
    
    adicionarNaFila(usuario1)
    adicionarNaFila(usuario2)
    
    ret = removerDaFila("U9")
    assert ret == -1
    assert tamanhoFila() == 2

def teste_remocao_cabeca():
    usuario1 = {"login": "U1", "tipo": 1}
    usuario2 = {"login": "U2", "tipo": 2}
    usuario3 = {"login": "U3", "tipo": 3}
    
    adicionarNaFila(usuario1)
    adicionarNaFila(usuario2)
    adicionarNaFila(usuario3)
    
    ret = removerDaFila("U1")  # Remove o primeiro (prioridade 1)
    assert ret == 0
    assert consultarPosicaoNaFila("U2") == 1  # U2 agora é o primeiro
    assert tamanhoFila() == 2

def teste_remocao_cauda():
    usuario1 = {"login": "U1", "tipo": 1}
    usuario2 = {"login": "U2", "tipo": 2}
    usuario3 = {"login": "U3", "tipo": 3}
    
    adicionarNaFila(usuario1)
    adicionarNaFila(usuario2)
    adicionarNaFila(usuario3)
    
    ret = removerDaFila("U3")  # Remove o último (prioridade 3)
    assert ret == 0
    assert consultarPosicaoNaFila("U2") == 2  # U2 agora é o último
    assert tamanhoFila() == 2

def teste_remocao_intermediario():
    usuario1 = {"login": "U1", "tipo": 1}
    usuario2 = {"login": "U2", "tipo": 2}
    usuario3 = {"login": "U3", "tipo": 3}
    
    adicionarNaFila(usuario1)
    adicionarNaFila(usuario2)
    adicionarNaFila(usuario3)
    
    ret = removerDaFila("U2")  # Remove o do meio (prioridade 2)
    assert ret == 0
    assert consultarPosicaoNaFila("U1") == 1
    assert consultarPosicaoNaFila("U3") == 2
    assert tamanhoFila() == 2

def teste_retorna_primeiro():
    assert retornaPrimeiro() is None
    
    usuario = {"login": "U1", "tipo": 1}
    adicionarNaFila(usuario)
    
    primeiro = retornaPrimeiro()
    assert isinstance(primeiro, dict)
    assert primeiro["login"] == "U1"
    # Verifica que não foi removido
    assert tamanhoFila() == 1

def teste_tamanho_fila():
    assert tamanhoFila() == 0
    
    usuario1 = {"login": "U1", "tipo": 1}
    usuario2 = {"login": "U2", "tipo": 2}
    
    adicionarNaFila(usuario1)
    assert tamanhoFila() == 1
    
    adicionarNaFila(usuario2)
    assert tamanhoFila() == 2
    
    removerDaFila("U1")
    assert tamanhoFila() == 1

def teste_inserir_usuario_ja_presente():
    usuario = {"login": "U1", "tipo": 1}
    ret1 = adicionarNaFila(usuario)
    ret2 = adicionarNaFila(usuario)
    assert ret2 == -1

def test_salvar_fila_em_csv(tmp_path):
    """(15) Verifica se salvar_fila_em_csv grava arquivo com ordem e conteúdo corretos."""
    # prepara fila
    adicionarNaFila({"login": "U1", "tipo": 1})
    adicionarNaFila({"login": "U2", "tipo": 2})
    csv_path = tmp_path / "subdir" / "fila.csv"
    salvar_fila_em_csv(str(csv_path))
    # lê de volta
    with open(csv_path, newline="", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f.readlines()]
    assert linhas == ["U1,1", "U2,2"]


def test_carregar_fila_de_csv(tmp_path):
    """(17) Lê CSV existente e popula _FILA na ordem correta."""
    csv_path = tmp_path / "fila.csv"
    csv_path.write_text("U1,1\nU2,2\n", encoding="utf-8")
    carregar_fila_de_csv(str(csv_path))
    assert tamanhoFila() == 2
    assert consultarPosicaoNaFila("U1") == 1
    assert consultarPosicaoNaFila("U2") == 2


def test_carregar_fila_csv_inexistente(tmp_path):
    """(19) Garantir que arquivo ausente não lança exceção e fila permanece vazia."""
    inexistente = tmp_path / "nao_existe" / "fila.csv"
    # certifica‑se de que não há arquivo
    if inexistente.exists():
        os.remove(inexistente)
    carregar_fila_de_csv(str(inexistente))  # não deve levantar
    assert tamanhoFila() == 0
