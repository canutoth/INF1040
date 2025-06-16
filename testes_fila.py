import pytest
from fila import (
    inicializarFila,
    consultarPosicaoNaFila,
    adicionarNaFila,
    removerDaFila,
    ordenarFilaPorPrioridade,
    retornaPrimeiro,
)

def teste_inicializacao_fila_vazia():
    fila = inicializarFila()
    assert isinstance(fila, list)
    assert len(fila) == 0

def teste_consultar_fila_vazia():
    assert consultarPosicaoNaFila([], "U1") == -1

def teste_adicionar_na_fila_vazia():
    fila = []
    usuario = {"login": "U1", "tipo": 1}
    ret = adicionarNaFila(fila, usuario)
    assert ret == 0
    assert len(fila) == 1
    assert fila[0]["login"] == "U1"

def teste_consultar_em_fila_com_um_elemento():
    fila = [{"login": "U1", "tipo": 1}]
    assert consultarPosicaoNaFila(fila, "U1") == 1

def teste_consultar_usuario_inexistente():
    fila = [{"login": "U1", "tipo": 1}]
    assert consultarPosicaoNaFila(fila, "U9") == -1

def teste_rejeicao_de_duplicata():
    fila = [{"login": "U1", "tipo": 1}]
    ret = adicionarNaFila(fila, {"login": "U1", "tipo": 1})
    assert ret == -1
    assert len(fila) == 1

def teste_ordenacao_por_prioridade():
    fila = [
        {"login": "U1", "tipo": 3},
        {"login": "U2", "tipo": 2},
        {"login": "U3", "tipo": 1},
    ]
    ordenarFilaPorPrioridade(fila)
    assert [u["login"] for u in fila] == ["U3", "U2", "U1"]

def teste_preservacao_ordem_mesma_prioridade():
    fila = [
        {"login": "U1", "tipo": 2},  # chegou antes
        {"login": "U2", "tipo": 2},
    ]
    ordenarFilaPorPrioridade(fila)
    assert [u["login"] for u in fila] == ["U1", "U2"]

def teste_ordenacao_idempotente_em_fila_vazia():
    fila = []
    ordenarFilaPorPrioridade(fila)
    assert fila == []

def teste_ordenacao_idempotente_em_fila_um_elemento():
    fila = [{"login": "U1", "tipo": 1}]
    ordenarFilaPorPrioridade(fila)
    assert fila == [{"login": "U1", "tipo": 1}]

def teste_remocao_usuario_inexistente():
    fila = [
        {"login": "U1", "tipo": 1},
        {"login": "U2", "tipo": 2},
    ]
    ret = removerDaFila(fila, "U9")
    assert ret == -1
    assert len(fila) == 2

def teste_remocao_cabeca():
    fila = [
        {"login": "U1", "tipo": 1},
        {"login": "U2", "tipo": 2},
        {"login": "U3", "tipo": 3},
    ]
    ret = removerDaFila(fila, "U1")
    assert ret == 0
    assert fila[0]["login"] == "U2"
    assert len(fila) == 2

def teste_remocao_cauda():
    fila = [
        {"login": "U1", "tipo": 1},
        {"login": "U2", "tipo": 2},
        {"login": "U3", "tipo": 3},
    ]
    ret = removerDaFila(fila, "U3")
    assert ret == 0
    assert fila[-1]["login"] == "U2"
    assert len(fila) == 2

def teste_remocao_intermediario():
    fila = [
        {"login": "U1", "tipo": 1},
        {"login": "U2", "tipo": 2},
        {"login": "U3", "tipo": 3},
    ]
    ret = removerDaFila(fila, "U2")
    assert ret == 0
    assert [u["login"] for u in fila] == ["U1", "U3"]
    assert len(fila) == 2

def teste_retorna_primeiro():
    assert retornaPrimeiro([]) is None
    fila = [{"login": "U1", "tipo": 1}]
    primeiro = retornaPrimeiro(fila)
    assert isinstance(primeiro, dict)
    assert primeiro["login"] == "U1"