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

# ---------------------------------------------------------------------------
def test_ocupaVagaPorId_falha_ja_ocupada():
    vs = [vaga_mod.nova_vaga(1)]
    assert vaga_mod.ocupar(vs[0], "U1")          # ocupa primeiro
    ok = vaga_mod.ocupaVagaPorId(vs, 1, "U2")    # tenta de novo
    assert not ok                                # deve falhar
    assert vs[0]["estado"] == "U1"               # login original intacto

# ---------------------------------------------------------------------------
def test_liberar_vaga_ja_livre():
    v = vaga_mod.nova_vaga(5)                    # já livre
    vaga_mod.liberar(v)                          # chamada idempotente
    assert vaga_mod.estaLivre(v) and v["estado"] == 0

# ---------------------------------------------------------------------------
def test_estaOcupadaPor_login_errado():
    """Vaga ocupada, mas consulta com login diferente → False."""
    v = vaga_mod.nova_vaga(6)
    assert vaga_mod.ocupar(v, "U1")
    assert not vaga_mod.estaOcupadaPor(v, "U2")

# ---------------------------------------------------------------------------
def test_getId_vaga_livre():
    """Testa getId com vaga recém-criada."""
    v = vaga_mod.nova_vaga(10)
    assert vaga_mod.getId(v) == 10

# ---------------------------------------------------------------------------
def test_getId_vaga_ocupada():
    """Testa getId com vaga ocupada - ID não deve mudar."""
    v = vaga_mod.nova_vaga(25)
    vaga_mod.ocupar(v, "U5")
    assert vaga_mod.getId(v) == 25

# ---------------------------------------------------------------------------
def test_getEstado_vaga_livre():
    """Testa getEstado com vaga livre."""
    v = vaga_mod.nova_vaga(7)
    assert vaga_mod.getEstado(v) == 0

# ---------------------------------------------------------------------------
def test_getEstado_vaga_ocupada():
    """Testa getEstado com vaga ocupada."""
    v = vaga_mod.nova_vaga(8)
    vaga_mod.ocupar(v, "U3")
    assert vaga_mod.getEstado(v) == "U3"

# ---------------------------------------------------------------------------
def test_getEstado_apos_liberar():
    """Testa getEstado após ocupar e liberar vaga."""
    v = vaga_mod.nova_vaga(9)
    
    # Estado inicial: livre
    assert vaga_mod.getEstado(v) == 0
    
    # Após ocupar
    vaga_mod.ocupar(v, "U4")
    assert vaga_mod.getEstado(v) == "U4"
    
    # Após liberar
    vaga_mod.liberar(v)
    assert vaga_mod.getEstado(v) == 0

# ---------------------------------------------------------------------------
def test_getEstado_multiplas_ocupacoes():
    """Testa getEstado com diferentes logins."""
    v = vaga_mod.nova_vaga(11)
    
    # Ocupa com primeiro usuário
    vaga_mod.ocupar(v, "admin")
    assert vaga_mod.getEstado(v) == "admin"
    
    # Libera e ocupa com segundo usuário
    vaga_mod.liberar(v)
    vaga_mod.ocupar(v, "user123")
    assert vaga_mod.getEstado(v) == "user123"