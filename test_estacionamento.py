import io
import csv
import builtins
import pytest
import vagas as vaga_mod
import estacionamento as est_mod

def _mock_est(*pos, **kw):
    """
    Gera um estacionamento de teste.

    Aceita as combinações exigidas pelos testes:

        _mock_est(livres=2, ocupadas=[1])
        _mock_est(qtd_vagas=3, ocupadas=[1, 2])
        _mock_est(livres=1, ocupadas=1)               # vaga 1 livre, vaga 2 ocupada
        _mock_est("Bloco X", livres=1, ocupadas=1)     # nome posicional
        _mock_est(nome="A")                            # alias 'nome='
        _mock_est("A")                                 # nome posicional + 1 vaga livre

    Regras:
      • `ocupadas=int`  → esse número de vagas ocupadas, logo após as livres.
      • `ocupadas=list` → ocupa exatamente esses ids.
      • Se só `qtd_vagas` for informado, livres = qtd_vagas – ocupadas.
    """
    # ───── nome do estacionamento ─────────────────────────────────────────
    if pos:
        name = pos[0]
    else:                                  # pode vir como nome= ou name=
        name = kw.pop("nome", kw.pop("name", "Mock"))

    livres     = kw.pop("livres", None)
    ocupadas   = kw.pop("ocupadas", None)
    qtd_vagas  = kw.pop("qtd_vagas", None)
    if kw:
        raise TypeError(f"parâmetros desconhecidos: {kw.keys()}")

    # normaliza 'ocupadas'
    if ocupadas is None:
        ocupadas = []
    if isinstance(ocupadas, int):
        ocupadas_qtd = ocupadas
        ocupadas = []
    else:
        ocupadas_qtd = None

    # resolve livres quando só qtd_vagas foi passado
    if livres is None:
        if qtd_vagas is None:
            livres = 1                      # default mínimo
        else:
            livres = qtd_vagas - len(ocupadas) - (ocupadas_qtd or 0)
    if livres < 0:
        raise ValueError("inconsistência entre livres/ocupadas/qtd_vagas")

    # se 'ocupadas' era número, define ids logo após as vagas livres
    if ocupadas_qtd is not None:
        ocupadas = list(range(livres + 1, livres + ocupadas_qtd + 1))

    # ───── construção do dicionário-estacionamento ───────────────────────
    est = est_mod.novo_estacionamento(name)

    # 1) adiciona vagas LIVRES primeiro (ids 1,2,… que não estejam em ocupadas)
    vid = 1
    livros_rest = livres
    while livros_rest:
        if vid not in ocupadas:
            est_mod.adicionar_vaga(est, vaga_mod.nova_vaga(vid))
            livros_rest -= 1
        vid += 1

    # 2) adiciona vagas OCUPADAS
    for vid in ocupadas:
        v = vaga_mod.nova_vaga(vid)
        vaga_mod.ocupar(v, f"U{vid}")
        est_mod.adicionar_vaga(est, v)

    return est

def test_novo_estacionamento_estrutura():
    est = est_mod.novo_estacionamento("Z")
    assert est == {"nome": "Z", "vagas": []}

def test_adicionar_vaga_insere_em_ordem():
    est = est_mod.novo_estacionamento("Z")
    v1, v2 = vaga_mod.nova_vaga(1), vaga_mod.nova_vaga(2)
    est_mod.adicionar_vaga(est, v1)
    est_mod.adicionar_vaga(est, v2)
    assert est["vagas"] == [v1, v2]

# get_vaga_disponivel com est vazio
def test_get_vaga_disponivel_sem_lista():
    est = est_mod.novo_estacionamento("Vazio")
    assert est_mod.get_vaga_disponivel(est) is None

# criar_estacionamentos_de_csv caminho inexistente
def test_criar_estacionamentos_csv_inexistente(tmp_path, capsys):
    caminho = tmp_path / "nao_existe.csv"
    ests = est_mod.criar_estacionamentos_de_csv(str(caminho))
    out = capsys.readouterr().out
    assert "não encontrado" in out.lower()
    assert ests == []
    
# ---------------------------------------------------------------------------
def teste_vagas_livres_varredura():
    est = _mock_est(livres=3, ocupadas=[1, 3])  # total 5
    assert est_mod.vagas_livres(est) == 3

# ---------------------------------------------------------------------------
def teste_get_vaga_disponivel_retorna_primeira_livre():
    est = _mock_est(livres=2, ocupadas=[1])     # total 3
    vaga = est_mod.get_vaga_disponivel(est)
    assert vaga["id"] == 2

# ---------------------------------------------------------------------------
def teste_get_vaga_disponivel_sem_vagas():
    est = _mock_est(qtd_vagas=2, ocupadas=[1, 2])
    assert est_mod.get_vaga_disponivel(est) is None

# ---------------------------------------------------------------------------
def teste_ocupar_vaga_por_login_sucesso():
    est = _mock_est(qtd_vagas=2, ocupadas=[1])
    ok, vid = est_mod.ocupar_vaga_por_login(est, "U9")
    assert ok and vid == 2
    # agora não deve haver vagas livres
    assert est_mod.get_vaga_disponivel(est) is None

# ---------------------------------------------------------------------------
def teste_ocupar_vaga_por_login_falha():
    est = _mock_est(qtd_vagas=1, ocupadas=[1])
    ok, vid = est_mod.ocupar_vaga_por_login(est, "U9")
    assert not ok and vid is None

# ---------------------------------------------------------------------------
def teste_liberar_vaga_de_sucesso():
    est = _mock_est(qtd_vagas=3, ocupadas=[2])
    user = {"login": "U2", "tipo": 1}
    vid = est_mod.liberar_vaga_de(est, user)
    assert vid == 2
    assert est_mod.vagas_livres(est) == 3

# ---------------------------------------------------------------------------
def teste_liberar_vaga_de_usuario_sem_vaga():
    est = _mock_est(qtd_vagas=3, ocupadas=[1])
    user = {"login": "U9", "tipo": 1}
    vid = est_mod.liberar_vaga_de(est, user)
    assert vid is None
    assert est_mod.vagas_livres(est) == 2

# ---------------------------------------------------------------------------
def teste_listar_estacionamentos_saida(capsys):
    ests = [
        _mock_est(qtd_vagas=2, ocupadas=[1], name="Bloco A"),
        _mock_est(qtd_vagas=3, ocupadas=[],  name="Bloco B"),
    ]
    est_mod.listar_estacionamentos(ests)
    capt = capsys.readouterr().out
    assert "Bloco A" in capt and "1" in capt      # 1 vaga livre em A
    assert "Bloco B" in capt and "3" in capt      # 3 vagas livres em B

# ---------------------------------------------------------------------------
def test_buscar_vaga_por_login_sucesso():
    est = _mock_est(livres=1, ocupadas=1)  # vaga id 2 ocupada por U2
    vaga = est_mod.buscar_vaga_por_login(est, "U2")
    assert vaga and vaga["id"] == 2
    assert est_mod.buscar_vaga_por_login(est, "UX") is None


# ---------------------------------------------------------------------------
def test_listar_status_vagas_captura_stdout(capsys):
    est = _mock_est("Bloco X", livres=1, ocupadas=1)
    est_mod.listar_status_vagas(est)
    out = capsys.readouterr().out
    assert "Bloco X" in out and "Livre" in out and "Ocupada por" in out


# ---------------------------------------------------------------------------
def test_verificar_status_vaga():
    est = _mock_est(livres=1, ocupadas=1)  # vagas 1 (livre) e 2 (ocupada)
    assert est_mod.verificar_status_vaga(est, 1).endswith("Livre")
    assert "Ocupada por" in est_mod.verificar_status_vaga(est, 2)
    assert est_mod.verificar_status_vaga(est, 99) == "ID de vaga inválido."


# ---------------------------------------------------------------------------
def test_salvar_estado_em_csv():
    est = _mock_est("Bloco CSV", livres=1, ocupadas=1)
    buf = io.StringIO()
    writer = csv.writer(buf)
    est_mod.salvar_estado_em_csv(est, writer)
    buf.seek(0)
    linha = next(csv.reader(buf))
    # Exemplo esperado: ["Bloco CSV", "0", "U2"]
    assert linha[0] == "Bloco CSV"
    assert linha[1] == "0"            # primeira vaga livre
    assert linha[2] == "U2"           # segunda vaga ocupada


# ---------------------------------------------------------------------------
def test_criar_estacionamentos_de_csv(tmp_path):
    csv_path = tmp_path / "ests.csv"
    csv_path.write_text("Est1,0,U1\nEst2,0,0\n")
    ests = est_mod.criar_estacionamentos_de_csv(str(csv_path))
    nomes = {e["nome"] for e in ests}
    assert nomes == {"Est1", "Est2"}
    est1 = next(e for e in ests if e["nome"] == "Est1")
    assert est_mod.vagas_livres(est1) == 1    # uma livre, uma ocupada


# ---------------------------------------------------------------------------
def test_selecionar_estacionamento(monkeypatch, capsys):
    ests = [_mock_est("A"), _mock_est("B")]
    # 1) escolha inválida → repete
    inputs = iter(["99", "2"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    est = est_mod.selecionar_estacionamento(ests)
    assert est["nome"] == "B"
    # 2) enter logo de cara → cancela
    monkeypatch.setattr(builtins, "input", lambda _: "")
    est_none = est_mod.selecionar_estacionamento(ests)
    assert est_none is None

# ---------------------------------------------------------------------------
def test_get_nome():
    est = _mock_est("Bloco CSV", livres=1, ocupadas=1)
    assert est_mod.getNome(est) == "Bloco CSV"