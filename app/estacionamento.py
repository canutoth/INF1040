<<<<<<< HEAD:app/estacionamento.py
import csv
import vagas as vaga_mod

"""
    Nome: novo_estacionamento(nome)

    Objetivo:
        Instanciar um registro-estacionamento vazio.

    Acoplamento:
        - nome: str — identificador do estacionamento.
        - retorno: dict {"nome": str, "vagas": list[dict]}.

    Descrição:
        Retorna dicionário com 'nome' e lista 'vagas' vazia.

    Hipóteses:
        - Nome não vazio, único no contexto do sistema.

    Restrições:
        - Não cria vagas automaticamente.
    """
def novo_estacionamento(nome: str) -> dict:
    return {"nome": nome, "vagas": []}

"""
    Nome: adicionar_vaga(est, vaga)

    Objetivo:
        Anexar nova vaga ao estacionamento.

    Condições de Acoplamento:
        AE: 'vaga' é dicionário gerado por vaga_mod.nova_vaga().
        AS: vaga inserida em est['vagas'].

    Restrições:
        - Não verifica duplicidade de ID.
    """
def adicionar_vaga(est: dict, vaga: dict) -> None:
    est["vagas"].append(vaga)

"""
    Nome: get_vaga_disponivel(est)

    Objetivo:
        Retornar o primeiro registro-vaga livre ou None.

    Hipóteses:
        - Prioridade = ordem da lista.
    """
def get_vaga_disponivel(est: dict):
    return next((v for v in est["vagas"] if vaga_mod.estaLivre(v)), None)

"""
    Nome: buscar_vaga_por_login(est, login)

    Objetivo:
        Localizar vaga ocupada por determinado usuário.

    Retorno:
        dict | None.
    """
def buscar_vaga_por_login(est: dict, login: str):
    return next((v for v in est["vagas"] if vaga_mod.estaOcupadaPor(v, login)), None)

"""
    Nome: liberar_vaga_de(est, usuario)

    Objetivo:
        Liberar a vaga ocupada por 'usuario'.

    Retorno:
        int | None — id da vaga liberada ou None se não encontrada.
    """
def liberar_vaga_de(est: dict, usuario: dict):
    v = buscar_vaga_por_login(est, usuario["login"])
    if v:
        vaga_mod.liberar(v)
        return vaga_mod.getId(v)
    return None

"""
    Nome: ocupar_vaga_por_login(est, login)

    Objetivo:
        Tentar ocupar primeira vaga livre.

    Retorno:
        tuple(bool, int|None) — (sucesso, id_vaga ou None)
    """
def ocupar_vaga_por_login(est: dict, login: str):
    v = get_vaga_disponivel(est)
    if v and vaga_mod.ocupar(v, login):
        return True, vaga_mod.getId(v)
    return False, None

"""
    Nome: vagas_livres(est)

    Objetivo:
        Contar vagas livres no estacionamento.
    """
def vagas_livres(est: dict) -> int:
    return sum(1 for v in est["vagas"] if vaga_mod.estaLivre(v))

"""
    Nome: listar_status_vagas(est)

    Objetivo:
        Imprimir estado de cada vaga no console.
    """
def listar_status_vagas(est: dict) -> None:
    print(f"\nStatus das vagas no {est['nome']}:")
    for v in est["vagas"]:
        print(vaga_mod.status(v))

"""
    Nome: verificar_status_vaga(est, id_vaga)

    Objetivo:
        Obter string de status da vaga de id_vaga.
    """
def verificar_status_vaga(est: dict, id_vaga: int) -> str:
    v = next((x for x in est["vagas"] if vaga_mod.getId(x) == id_vaga), None)
    return vaga_mod.status(v) if v else "ID de vaga inválido."

"""
    Nome: salvar_estado_em_csv(est, writer)

    Objetivo:
        Persistir linha CSV: [nome, estado1, estado2, …].
    """
def salvar_estado_em_csv(est: dict, writer) -> None:
    linha = [est["nome"]] + [
        (vaga_mod.getEstado(v) if not vaga_mod.estaLivre(v) else "0") for v in est["vagas"]
    ]
    writer.writerow(linha)

"""
    Nome: criar_estacionamentos_de_csv(caminho_csv)

    Objetivo:
        Construir lista de estacionamentos + vagas a partir de arquivo CSV.

    Formato do CSV:
        nome_est,login_vaga1,login_vaga2,...
        • "0" indica vaga livre.
    """
def criar_estacionamentos_de_csv(caminho_csv: str) -> list[dict]:
    ests: list[dict] = []
    try:
        with open(caminho_csv, newline='', encoding="utf-8") as f:
            for row in csv.reader(f):
                if not row:
                    continue
                est = novo_estacionamento(row[0])
                for i, estado in enumerate(row[1:], 1):
                    v = vaga_mod.nova_vaga(i)
                    if estado.strip() != "0":
                        vaga_mod.ocupar(v, estado.strip())
                    adicionar_vaga(est, v)
                ests.append(est)
    except FileNotFoundError:
        print(f"Arquivo {caminho_csv} não encontrado.")
    return ests

"""
    Nome: listar_estacionamentos(ests)

    Objetivo:
        Exibir nome e vagas livres de cada estacionamento.
    """
def listar_estacionamentos(ests: list[dict]) -> None:
    print("\nEstacionamentos disponíveis:")
    for idx, e in enumerate(ests, 1):
        print(f"{idx}. {e['nome']} – Vagas livres: {vagas_livres(e)}")

"""
    Nome: selecionar_estacionamento(ests)

    Objetivo:
        Permitir seleção de estacionamento pelo usuário.
    """
def selecionar_estacionamento(ests: list[dict]):
    if not ests:
        print("⚠️ Nenhum estacionamento disponível.")
        return None
    while True:
        listar_estacionamentos(ests)
        esc = input("Escolha (número) › ").strip()
        if not esc:
            return None
        try:
            return ests[int(esc) - 1]
        except (ValueError, IndexError):
            print("⚠️ Opção inválida. Tente novamente ou Enter para cancelar.")

"""
    Nome: getNome(estacionamento)

    Objetivo:
        Obter o nome de um estacionamento sem expor a estrutura interna.

    Acoplamento:
        - estacionamento: dict — objeto estacionamento.
        - retorno: str — nome do estacionamento.

    Descrição:
        Função de acesso que encapsula o campo "nome" do estacionamento.
"""
def getNome(estacionamento: dict) -> str:
    """Retorna o nome do estacionamento de forma encapsulada."""
    return estacionamento["nome"]
=======
import csv
import vagas as vaga_mod

# ---------------------------------------------------------------------------
# FUNCOES INTERNAS AO MODULO
"""
    Nome: _novo_estacionamento(nome)

    Objetivo:
        Instanciar um registro-estacionamento vazio.

    Acoplamento:
        - nome: str — identificador do estacionamento.
        - retorno: dict {"nome": str, "vagas": list[dict]}.

    Descrição:
        Retorna dicionário com 'nome' e lista 'vagas' vazia.

    Hipóteses:
        - Nome não vazio, único no contexto do sistema.

    Restrições:
        - Não cria vagas automaticamente.
    """
def _novo_estacionamento(nome: str) -> dict:
    return {"nome": nome, "vagas": []}

"""
    Nome: adicionar_vaga(est, vaga)

    Objetivo:
        Anexar nova vaga ao estacionamento.

    Condições de Acoplamento:
        AE: 'vaga' é dicionário gerado por vaga_mod.nova_vaga().
        AS: vaga inserida em est['vagas'].

    Restrições:
        - Não verifica duplicidade de ID.
    """
def _adicionar_vaga(est: dict, vaga: dict) -> None:
    est["vagas"].append(vaga)

"""    
    Nome: _vagas_livres(est)

    Objetivo:
        Contar vagas livres no estacionamento.
    """
def _vagas_livres(est: dict) -> int:
    return sum(1 for v in est["vagas"] if vaga_mod.estaLivre(v))

"""
    Nome: _verificar_status_vaga(est, id_vaga)

    Objetivo:
        Obter string de status da vaga de id_vaga.
    """
def _verificar_status_vaga(est: dict, id_vaga: int) -> str:
    v = next((x for x in est["vagas"] if vaga_mod.getId(x) == id_vaga), None)
    return vaga_mod.status(v) if v else "ID de vaga inválido."

"""
    Nome: _listar_status_vagas(est)

    Objetivo:
        Imprimir estado de cada vaga no console.
    """
def _listar_status_vagas(est: dict) -> None:
    print(f"\nStatus das vagas no {est['nome']}:")
    for v in est["vagas"]:
        print(vaga_mod.status(v))

# ---------------------------------------------------------------------------
# APIs Publicas
def novo_estacionamento(nome: str):
    return _novo_estacionamento(nome)

def adicionar_vaga(est, vaga):
    _adicionar_vaga(est, vaga)

def vagas_livres(est):
    return _vagas_livres(est)

def listar_status_vagas(est):
    return _listar_status_vagas(est)
"""
    Nome: get_vaga_disponivel(est)

    Objetivo:
        Retornar o primeiro registro-vaga livre ou None.

    Hipóteses:
        - Prioridade = ordem da lista.
    """
def get_vaga_disponivel(est: dict):
    return next((v for v in est["vagas"] if vaga_mod.estaLivre(v)), None)

"""
    Nome: buscar_vaga_por_login(est, login)

    Objetivo:
        Localizar vaga ocupada por determinado usuário.

    Retorno:
        dict | None.
    """
def buscar_vaga_por_login(est: dict, login: str):
    return next((v for v in est["vagas"] if vaga_mod.estaOcupadaPor(v, login)), None)

"""
    Nome: liberar_vaga_de(est, usuario)

    Objetivo:
        Liberar a vaga ocupada por 'usuario'.

    Retorno:
        int | None — id da vaga liberada ou None se não encontrada.
    """
def liberar_vaga_de(est: dict, usuario: dict):
    v = buscar_vaga_por_login(est, usuario["login"])
    if v:
        vaga_mod.liberar(v)
        return vaga_mod.getId(v)
    return None

"""
    Nome: ocupar_vaga_por_login(est, login)

    Objetivo:
        Tentar ocupar primeira vaga livre.

    Retorno:
        tuple(bool, int|None) — (sucesso, id_vaga ou None)
    """
def ocupar_vaga_por_login(est: dict, login: str):
    v = get_vaga_disponivel(est)
    if v and vaga_mod.ocupar(v, login):
        return True, vaga_mod.getId(v)
    return False, None

"""
    Nome: salvar_estado_em_csv(est, writer)

    Objetivo:
        Persistir linha CSV: [nome, estado1, estado2, …].
    """
def salvar_estado_em_csv(est: dict, writer) -> None:
    linha = [est["nome"]] + [
        (vaga_mod.getEstado(v) if not vaga_mod.estaLivre(v) else "0") for v in est["vagas"]
    ]
    writer.writerow(linha)

"""
    Nome: criar_estacionamentos_de_csv(caminho_csv)

    Objetivo:
        Construir lista de estacionamentos + vagas a partir de arquivo CSV.

    Formato do CSV:
        nome_est,login_vaga1,login_vaga2,...
        • "0" indica vaga livre.
    """
def criar_estacionamentos_de_csv(caminho_csv: str) -> list[dict]:
    ests: list[dict] = []
    try:
        with open(caminho_csv, newline='', encoding="utf-8") as f:
            for row in csv.reader(f):
                if not row:
                    continue
                est = _novo_estacionamento(row[0])
                for i, estado in enumerate(row[1:], 1):
                    v = vaga_mod.nova_vaga(i)
                    if estado.strip() != "0":
                        vaga_mod.ocupar(v, estado.strip())
                    _adicionar_vaga(est, v)
                ests.append(est)
    except FileNotFoundError:
        print(f"Arquivo {caminho_csv} não encontrado.")
    return ests

"""
    Nome: listar_estacionamentos(ests)

    Objetivo:
        Exibir nome e vagas livres de cada estacionamento.
    """
def listar_estacionamentos(ests: list[dict]) -> None:
    print("\nEstacionamentos disponíveis:")
    for idx, e in enumerate(ests, 1):
        print(f"{idx}. {e['nome']} – Vagas livres: {_vagas_livres(e)}")

"""
    Nome: selecionar_estacionamento(ests)

    Objetivo:
        Permitir seleção de estacionamento pelo usuário.
    """
def selecionar_estacionamento(ests: list[dict]):
    if not ests:
        print("⚠️ Nenhum estacionamento disponível.")
        return None
    while True:
        listar_estacionamentos(ests)
        esc = input("Escolha (número) › ").strip()
        if not esc:
            return None
        try:
            return ests[int(esc) - 1]
        except (ValueError, IndexError):
            print("⚠️ Opção inválida. Tente novamente ou Enter para cancelar.")

"""
    Nome: getNome(estacionamento)

    Objetivo:
        Obter o nome de um estacionamento sem expor a estrutura interna.

    Acoplamento:
        - estacionamento: dict — objeto estacionamento.
        - retorno: str — nome do estacionamento.

    Descrição:
        Função de acesso que encapsula o campo "nome" do estacionamento.
"""
def getNome(estacionamento: dict) -> str:
    """Retorna o nome do estacionamento de forma encapsulada."""
    return estacionamento["nome"]

__all__ = [
    "get_vaga_disponivel",
    "buscar_vaga_por_login",
    "liberar_vaga_de",
    "ocupar_vaga_por_login",
    "salvar_estado_em_csv",
    "criar_estacionamentos_de_csv",
    "listar_estacionamentos",
    "selecionar_estacionamento",
    "getNome",
]
>>>>>>> 6cc85dd154a8cd0119e83129a4d74f3ff9c8f22d:estacionamento.py
