"""
    Nome: nova_vaga(id_vaga)

    Objetivo:
        Criar e devolver um registro–vaga no formato dicionário.

    Acoplamento:
        - id_vaga: int — identificador único dentro do estacionamento.
        - retorno: dict — {"id": int, "estado": 0}.

    Condições de Acoplamento:
        AE: id_vaga inteiro positivo.
        AS: retorna dicionário com estado livre (0).

    Descrição:
        1) Monta dict {'id': id_vaga, 'estado': 0}.
        2) Retorna o dicionário.

    Hipóteses:
        - Cada estacionamento garante unicidade de id_vaga.

    Restrições:
        - Estado “0” representa vaga livre; qualquer string = login ocupado.
    """
def nova_vaga(id_vaga: int) -> dict:
    return {"id": id_vaga, "estado": 0}

"""
    Nome: estaLivre(vaga)

    Objetivo:
        Verificar se a vaga está livre.

    Acoplamento:
        - vaga: dict — registro gerado por nova_vaga().
        - retorno: bool.

    Descrição:
        Retorna True se vaga['estado'] == 0.
    """
def estaLivre(vaga: dict) -> bool:
    return vaga["estado"] == 0

"""
    Nome: estaOcupadaPor(vaga, login)

    Objetivo:
        Conferir se a vaga está ocupada pelo usuário `login`.

    Retorno:
        bool.
    """
def estaOcupadaPor(vaga: dict, login: str) -> bool:
    return vaga["estado"] == login

"""
    Nome: ocupar(vaga, login)

    Objetivo:
        Marcar a vaga como ocupada pelo login informado.

    Acoplamento:
        - retorno: bool — True se ocupação realizada.

    Descrição:
        1) Se estaLivre() → grava login em vaga['estado'] e retorna True.
        2) Caso contrário, retorna False.
    """
def ocupar(vaga: dict, login: str) -> bool:
    if estaLivre(vaga):
        vaga["estado"] = login
        return True
    return False

"""
    Nome: liberar(vaga)

    Objetivo:
        Tornar a vaga livre novamente (estado = 0).

    Retorno:
        None.
    """
def liberar(vaga: dict) -> None:
    vaga["estado"] = 0

"""
    Nome: status(vaga)

    Objetivo:
        Gerar string legível do estado atual da vaga.

    Retorno:
        str — "Vaga 01: Livre" ou "Vaga 01: Ocupada por <login>".
    """
def status(vaga: dict) -> str:
    if estaLivre(vaga):
        return f"Vaga {vaga['id']:02d}: Livre"
    return f"Vaga {vaga['id']:02d}: Ocupada por {vaga['estado']}"

"""
    Nome: ocupaVagaPorId(vagas, vaga_id, login)

    Objetivo:
        Localizar a vaga de id == vaga_id na lista e tentar ocupá-la.

    Acoplamento:
        - vagas: list[dict] — coleção de registros–vaga.
        - retorno: bool — True se ocupada com sucesso.

    Descrição:
        1) Busca vaga pelo id.
        2) Se não encontrada → False.
        3) Se encontrada → chamar ocupar(); retorna resultado.
    """
def ocupaVagaPorId(vagas: list[dict], vaga_id: int, login: str) -> bool:
    alvo = next((v for v in vagas if v["id"] == vaga_id), None)
    return ocupar(alvo, login) if alvo else False

"""
    Nome: getId(vaga)

    Objetivo:
        Obter o ID de uma vaga sem expor a estrutura interna.

    Acoplamento:
        
vaga: dict — registro vaga.
retorno: int — ID da vaga.

    Descrição:
        Função de acesso que encapsula o campo "id" da vaga.
"""
def getId(vaga: dict) -> int:
    """Retorna o ID da vaga de forma encapsulada."""
    return vaga["id"]

"""
    Nome: getEstado(vaga)

    Objetivo:
        Obter o estado de uma vaga sem expor a estrutura interna.

    Acoplamento:
        
vaga: dict — registro vaga.
retorno: int | str — estado da vaga (0 se livre, login se ocupada).

    Descrição:
        Função de acesso que encapsula o campo "estado" da vaga.
"""
def getEstado(vaga: dict):
    """Retorna o estado da vaga de forma encapsulada."""
    return vaga["estado"]
