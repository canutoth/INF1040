import pytest
import vagas as vaga_mod

# ---------------------------------------------------------------------------
def teste_nova_vaga_inicial_livre():
    v = vaga_mod.nova_vaga(1)
    assert v["id"] == 1
    assert vaga_mod.estaLivre(v)
    assert not vaga_mod.estaOcupadaPor(v, "U1")
    assert vaga_mod.status(v) == "Vaga 01: Livre"

# ---------------------------------------------------------------------------
def teste_ocupar_vaga_livre():
    v = vaga_mod.nova_vaga(2)
    ok = vaga_mod.ocupar(v, "U1")
    assert ok
    assert vaga_mod.estaOcupadaPor(v, "U1")
    assert not vaga_mod.estaLivre(v)
    assert vaga_mod.status(v) == "Vaga 02: Ocupada por U1"

# ---------------------------------------------------------------------------
def teste_ocupar_vaga_ja_ocupada():
    v = vaga_mod.nova_vaga(3)
    vaga_mod.ocupar(v, "U1")
    ok = vaga_mod.ocupar(v, "U2")
    assert not ok
    # estado não mudou
    assert vaga_mod.estaOcupadaPor(v, "U1")

# ---------------------------------------------------------------------------
def teste_liberar_vaga():
    v = vaga_mod.nova_vaga(4)
    vaga_mod.ocupar(v, "U9")
    vaga_mod.liberar(v)
    assert vaga_mod.estaLivre(v)
    assert vaga_mod.status(v) == "Vaga 04: Livre"

# ---------------------------------------------------------------------------
def teste_ocupaVagaPorId_sucesso():
    vs = [vaga_mod.nova_vaga(i) for i in range(1, 4)]
    ok = vaga_mod.ocupaVagaPorId(vs, 2, "U7")
    assert ok
    assert vs[1]["estado"] == "U7"

# ---------------------------------------------------------------------------
def teste_ocupaVagaPorId_falha_id_inexistente():
    vs = [vaga_mod.nova_vaga(i) for i in range(1, 3)]
    ok = vaga_mod.ocupaVagaPorId(vs, 99, "U7")
    assert not ok