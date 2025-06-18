import usuario

# ---------------------------- variável global da fila ------------------------
_FILA = []

"""
    Nome: consultarPosicaoNaFila(id_usuario)

    Objetivo:
        Retornar a posição (base 1) do usuário ou –1 se ausente.

    Acoplamento:
        - _FILA: list[dict] — cada dict tem 'login'.
        - id_usuario: str — login a procurar.
        - retorno: int.

    Condições de Acoplamento:
        AE: id_usuario não vazio.
        AS: devolve posição correta (idx + 1) ou –1.

    Descrição:
        Itera enumerate(_FILA); compara getLogin(u) com id_usuario.

    Hipóteses:
        - Logins são únicos.

    Restrições:
        - Busca O(n).
"""
def consultarPosicaoNaFila(id_usuario):
    for i, user in enumerate(_FILA):
        if usuario.getLogin(user) == id_usuario:
            return i + 1
    return -1

"""
    Nome: adicionarNaFila(usuario_obj)

    Objetivo:
        Inserir `usuario_obj` se ainda não estiver na fila.

    Acoplamento:
        - _FILA: list[dict].
        - usuario_obj: dict — chaves 'login', 'tipo'.
        - retorno: int — 0=sucesso, –1=já presente.

    Condições de Acoplamento:
        AE: getTipo(usuario_obj) ∈ {1,2,3}.
        AS: fila reordenada por prioridade após inserção.

    Descrição:
        1) Se login já presente → –1.
        2) append(usuario_obj) → ordenarFilaPorPrioridade() → 0.

    Hipóteses:
        - Logins são únicos por usuário.
        - usuario_obj é dict válido com campos obrigatórios.

    Restrições:
        - Busca O(n) para verificar duplicidade.
        - Ordenação O(n log n) após inserção.
"""
def adicionarNaFila(usuario_obj):
    if consultarPosicaoNaFila(usuario.getLogin(usuario_obj)) != -1:
        return -1

    _FILA.append(usuario_obj)
    ordenarFilaPorPrioridade()
    return 0

"""
    Nome: removerDaFila(id_usuario)

    Objetivo:
        Remover usuário cujo login == id_usuario.

    Acoplamento:
        - _FILA: list[dict].
        - id_usuario: str.
        - retorno: int — 0 removido, –1 não achou.

    Condições de Acoplamento:
        AE: id_usuario não vazio.
        AS: primeiro usuário com login correspondente é removido.

    Descrição:
        Percorre lista; del quando getLogin(u) coincide.

    Hipóteses:
        - Logins são únicos na fila.

    Restrições:
        - Busca e remoção O(n).
"""
def removerDaFila(id_usuario):
    for i, u in enumerate(_FILA):
        if usuario.getLogin(u) == id_usuario:
            del _FILA[i]
            return 0
    return -1

"""
    Nome: ordenarFilaPorPrioridade()

    Objetivo:
        Ordenar in-place pelo campo 'tipo':
        1 primeiro, depois 2.

    Acoplamento:
        - _FILA: list[dict].

    Condições de Acoplamento:
        AE: _FILA lista válida.
        AS: fila reordenada por prioridade.

    Descrição:
        list.sort(key=lambda u: getTipo(u)) — sort do Python é estável.

    Hipóteses:
        - Todos os usuários têm campo 'tipo' válido.
        - Tipos são valores numéricos ordenáveis.

    Restrições:
        - Ordenação O(n log n).
        - Modifica _FILA in-place.
"""
def ordenarFilaPorPrioridade():
    if len(_FILA) > 1:
        _FILA.sort(key=lambda u: usuario.getTipo(u))

"""
    Nome: retornaPrimeiro()

    Objetivo:
        Obter o primeiro elemento sem removê-lo.

    Acoplamento:
        - _FILA: list[dict].
        - retorno: dict | None.

    Condições de Acoplamento:
        AE: _FILA lista válida.
        AS: devolve primeiro elemento ou None se vazia.

    Descrição:
        Acessa _FILA[0] se não vazia, senão retorna None.

    Hipóteses:
        - Fila mantém ordenação por prioridade.

    Restrições:
        - Acesso O(1).
        - Não modifica a fila.
"""
def retornaPrimeiro():
    return _FILA[0] if _FILA else None

"""
    Nome: tamanhoFila()

    Objetivo:
        Retornar o número de usuários na fila.

    Acoplamento:
        - _FILA: list[dict].
        - retorno: int.

    Condições de Acoplamento:
        AE: _FILA lista válida.
        AS: devolve tamanho da fila.

    Descrição:
        Retorna len(_FILA).

    Hipóteses:
        - _FILA é lista Python válida.

    Restrições:
        - Acesso O(1).
        - Não modifica a fila.
"""
def tamanhoFila():
    return len(_FILA)

"""
    Nome: esvaziarFila()

    Objetivo:
        Limpar todos os elementos da fila.

    Acoplamento:
        - _FILA: list[dict].

    Condições de Acoplamento:
        AE: _FILA lista válida.
        AS: _FILA fica vazia.

    Descrição:
        Chama clear() na lista da fila.

    Restrições:
        - Chamada típica no final da aplicação.
"""
def esvaziarFila():
    _FILA.clear()