"""
    Nome: inicializarFila()

    Objetivo:
        Criar e devolver a estrutura de dados que representará a fila.

    Acoplamento:
        - retorno: list — lista Python vazia.

    Condições de Acoplamento:
        AE: chamada sem parâmetros.
        AS: devolve lista vazia, pronta para uso como fila.

    Descrição:
        1) Instancia lista []. 
        2) Retorna a lista.

    Hipóteses:
        - Chamada única na inicialização do sistema.

    Restrições:
        - Não persiste em disco; vive apenas em memória.
"""
def inicializarFila():
    # PASSO 1: criar nova lista vazia
    fila = []
    # AS: fila inicializada como lista vazia
    return fila

"""
    Nome: consultarPosicaoNaFila(fila, id_usuario)

    Objetivo:
        Retornar a posição (base 1) do usuário ou –1 se ausente.

    Acoplamento:
        - fila: list[dict] — cada dict tem 'login'.
        - id_usuario: str — login a procurar.
        - retorno: int.

    Condições de Acoplamento:
        AE: fila lista válida; id_usuario não vazio.
        AS: devolve posição correta ou –1.

    Descrição:
        Itera enumerate(fila); compara u['login'] com id_usuario.

    Hipóteses:
        - Logins são únicos.

    Restrições:
        - Busca O(n).
    """
def consultarPosicaoNaFila(fila, id_usuario):
    for i, usuario in enumerate(fila):
        if usuario["login"] == id_usuario:
            return i + 1
    return -1

"""
    Nome: adicionarNaFila(fila, usuario)

    Objetivo:
        Inserir `usuario` se ainda não estiver na fila.

    Acoplamento:
        - fila: list[dict].
        - usuario: dict — chaves 'login', 'tipo'.
        - retorno: int — 0=sucesso, –1=já presente.

    Condições de Acoplamento:
        AE: usuario['tipo'] ∈ {1,2,3}.
        AS: fila reordenada por prioridade após inserção.

    Descrição:
        1) Se login já presente → –1.
        2) append(usuario) → ordenarFilaPorPrioridade() → 0.
    """
def adicionarNaFila(fila, usuario):
    if consultarPosicaoNaFila(fila, usuario["login"]) != -1:
        return -1

    fila.append(usuario)
    ordenarFilaPorPrioridade(fila)
    return 0

"""
    Nome: removerDaFila(fila, id_usuario)

    Objetivo:
        Remover usuário cujo login == id_usuario.

    Acoplamento:
        - fila: list[dict].
        - id_usuario: str.
        - retorno: int — 0 removido, –1 não achou.

    Descrição:
        Percorre lista; del quando u['login'] coincide.
    """
def removerDaFila(fila, id_usuario):
    for i, u in enumerate(fila):
        if u["login"] == id_usuario:
            del fila[i]
            return 0
    return -1

"""
    Nome: ordenarFilaPorPrioridade(fila)

    Objetivo:
        Ordenar in-place pelo campo 'tipo':
        1 primeiro, depois 2, depois 3 (ordem estável).

    Acoplamento:
        - fila: list[dict].

    Descrição:
        list.sort(key=lambda u: u['tipo']) — sort do Python é estável.
    """
def ordenarFilaPorPrioridade(fila):
    if len(fila) > 1:
        fila.sort(key=lambda u: u["tipo"])

"""
    Nome: retornaPrimeiro(fila)

    Objetivo:
        Obter o primeiro elemento sem removê-lo.

    Retorno:
        dict | None.
    """
def retornaPrimeiro(fila):
    return fila[0] if fila else None