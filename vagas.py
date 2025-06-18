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
    - Estado "0" representa vaga livre; qualquer string = login ocupado.
"""


def nova_vaga(id_vaga: int) -> dict:
    return {"id": id_vaga, "estado": 0}


"""
    Nome: estaLivre(vaga)

    Objetivo:
        Verificar se a vaga está livre.

    Acoplamento:
        - vaga: dict — registro gerado por nova_vaga().
        - retorno: bool — True se livre, False caso contrário.

    Condições de Acoplamento:
        AE: vaga deve ser um dicionário válido com chave 'estado'.
        AS: retorna booleano indicando se vaga está livre.

    Descrição:
        1) Verifica se vaga['estado'] == 0.
        2) Retorna True se condição satisfeita, False caso contrário.

    Restrições:
        - Estado "0" representa vaga livre; qualquer string = login ocupado.
    """


def estaLivre(vaga: dict) -> bool:
    return vaga["estado"] == 0


"""
    Nome: estaOcupadaPor(vaga, login)

    Objetivo:
        Conferir se a vaga está ocupada pelo usuário específico.

    Acoplamento:
        - vaga: dict — registro gerado por nova_vaga().
        - login: str — identificador do usuário.
        - retorno: bool — True se ocupada pelo login, False caso contrário.

    Condições de Acoplamento:
        AE: vaga deve ser um dicionário válido; login deve ser string não vazia.
        AS: retorna booleano indicando se vaga está ocupada pelo login específico.

    Descrição:
        1) Compara vaga['estado'] com o login fornecido.
        2) Retorna True se iguais, False caso contrário.

    Restrições:
        - Comparação é case-sensitive.
        - Estado "0" representa vaga livre; qualquer string = login ocupado.
    """


def estaOcupadaPor(vaga: dict, login: str) -> bool:
    return vaga["estado"] == login


"""
    Nome: ocupar(vaga, login)

    Objetivo:
        Marcar a vaga como ocupada pelo login informado se estiver livre.

    Acoplamento:
        - vaga: dict — registro gerado por nova_vaga().
        - login: str — identificador do usuário.
        - retorno: bool — True se ocupação realizada, False caso contrário.

    Condições de Acoplamento:
        AE: vaga deve ser um dicionário válido; login deve ser string não vazia.
        AS: se vaga estava livre, fica ocupada pelo login e retorna True; 
            caso contrário, vaga inalterada e retorna False.

    Descrição:
        1) Verifica se estaLivre(vaga) retorna True.
        2) Se sim: grava login em vaga['estado'] e retorna True.
        3) Caso contrário: retorna False sem modificar a vaga.

    Restrições:
        - Só ocupa vaga se estiver livre (estado = 0).
        - Uma vez ocupada, vaga não pode ser ocupada por outro usuário.
    """


def ocupar(vaga: dict, login: str) -> bool:
    if estaLivre(vaga):
        vaga["estado"] = login
        return True
    return False


"""
    Nome: liberar(vaga)

    Objetivo:
        Tornar a vaga livre novamente, independente do estado atual.

    Acoplamento:
        - vaga: dict — registro gerado por nova_vaga().
        - retorno: None.

    Condições de Acoplamento:
        AE: vaga deve ser um dicionário válido com chave 'estado'.
        AS: vaga fica com estado livre (0).

    Descrição:
        1) Define vaga['estado'] = 0.
        2) Não retorna valor.

    Restrições:
        - Operação sempre bem-sucedida, independente do estado anterior.
        - Estado "0" representa vaga livre.
    """


def liberar(vaga: dict) -> None:
    vaga["estado"] = 0


"""
    Nome: status(vaga)

    Objetivo:
        Gerar string legível do estado atual da vaga.

    Acoplamento:
        - vaga: dict — registro gerado por nova_vaga().
        - retorno: str — descrição formatada do estado da vaga.

    Condições de Acoplamento:
        AE: vaga deve ser um dicionário válido com chaves 'id' e 'estado'.
        AS: retorna string formatada descrevendo o estado da vaga.

    Descrição:
        1) Se estaLivre(vaga): retorna "Vaga XX: Livre" (XX = id formatado com 2 dígitos).
        2) Caso contrário: retorna "Vaga XX: Ocupada por <login>".

    Restrições:
        - Estado "0" representa vaga livre; qualquer string = login ocupado.
    """


def status(vaga: dict) -> str:
    if estaLivre(vaga):
        return f"Vaga {vaga['id']:02d}: Livre"
    return f"Vaga {vaga['id']:02d}: Ocupada por {vaga['estado']}"


"""
    Nome: ocupaVagaPorId(vagas, vaga_id, login)

    Objetivo:
        Localizar a vaga de id específico na lista e tentar ocupá-la.

    Acoplamento:
        - vagas: list[dict] — coleção de registros–vaga.
        - vaga_id: int — identificador da vaga a ser ocupada.
        - login: str — identificador do usuário.
        - retorno: bool — True se ocupada com sucesso, False caso contrário.

    Condições de Acoplamento:
        AE: vagas deve ser lista de dicionários válidos; vaga_id inteiro positivo; 
            login string não vazia.
        AS: se vaga encontrada e livre, fica ocupada pelo login e retorna True; 
            caso contrário retorna False.

    Descrição:
        1) Busca na lista vagas o primeiro elemento com v["id"] == vaga_id.
        2) Se não encontrada: retorna False.
        3) Se encontrada: chama ocupar(vaga, login) e retorna o resultado.

    Hipóteses:
        - IDs de vagas são únicos dentro da lista.
        - Lista pode estar vazia ou não conter a vaga procurada.

    Restrições:
        - Só ocupa se vaga existir e estiver livre.
        - Busca para no primeiro elemento com ID correspondente.
    """


def ocupaVagaPorId(vagas: list[dict], vaga_id: int, login: str) -> bool:
    alvo = next((v for v in vagas if v["id"] == vaga_id), None)
    return ocupar(alvo, login) if alvo else False


"""
    Nome: getId(vaga)

    Objetivo:
        Obter o ID de uma vaga sem expor a estrutura interna do dicionário.

    Acoplamento:
        - vaga: dict — registro gerado por nova_vaga().
        - retorno: int — identificador único da vaga.

    Condições de Acoplamento:
        AE: vaga deve ser um dicionário válido com chave 'id'.
        AS: retorna o valor inteiro do ID da vaga.

    Descrição:
        1) Acessa vaga["id"] e retorna o valor.

    Restrições:
        - Função de acesso somente leitura (não modifica a vaga).
    """


def getId(vaga: dict) -> int:
    """Retorna o ID da vaga de forma encapsulada."""
    return vaga["id"]


"""
    Nome: getEstado(vaga)

    Objetivo:
        Obter o estado de uma vaga sem expor a estrutura interna do dicionário.

    Acoplamento:
        - vaga: dict — registro gerado por nova_vaga().
        - retorno: int | str — estado da vaga (0 se livre, login se ocupada).

    Condições de Acoplamento:
        AE: vaga deve ser um dicionário válido com chave 'estado'.
        AS: retorna o valor do estado (0 para livre, string para ocupada).

    Descrição:
        1) Acessa vaga["estado"] e retorna o valor.

    Restrições:
        - Função de acesso somente leitura (não modifica a vaga).
        - Estado "0" representa vaga livre; qualquer string = login ocupado.
    """


def getEstado(vaga: dict):
    """Retorna o estado da vaga de forma encapsulada."""
    return vaga["estado"]
