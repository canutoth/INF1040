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
        Retornar a posição (base 1) do usuário na fila ou –1 se não estiver.

    Acoplamento:
        - fila: list[Usuario] — fila vigente.
        - id_usuario: str     — login a localizar.
        - retorno: int        — posição (1,2,3,…) ou –1.

    Condições de Acoplamento:
        AE: fila é lista válida.
        AE: id_usuario é string não vazia.
        AS: devolve posição correta ou –1 se ausente.

    Descrição:
        Itera enumerate(fila); compara usuario.login com id_usuario; ao
        encontrar, retorna i + 1. Se varreu toda lista → –1.

    Hipóteses:
        - Cada objeto da fila expõe atributo .login.
"""
def consultarPosicaoNaFila(fila, id_usuario):
    # PASSO 1: verificar se fila existe e não está vazia
    if not fila:
        return -1

    # PASSO 2: percorrer lista do início ao fim
    for i, usuario in enumerate(fila):
        # PASSO 3: comparar id do usuário atual com id_usuario procurado
        if usuario.login == id_usuario:
            # AS: usuário encontrado, retorna posição (base 1)
            return i + 1

    # PASSO 4: usuário não encontrado após percorrer toda a fila
    return -1

"""
    Nome: adicionarNaFila(fila, usuario)

    Objetivo:
        Inserir `usuario` se ainda não estiver na fila.

    Acoplamento:
        - fila: list[Usuario].
        - usuario: Usuario — possui atributos .login e .tipo.
        - retorno: int — 0=sucesso, –1=já estava.

    Condições de Acoplamento:
        AE: usuario.tipo ∈ {1,2,3}.
        AS: fila recebe o usuário no final e é reordenada por prioridade.

    Descrição:
        1) Se usuario.login já presente → –1.
        2) append(usuario) e chamar ordenarFilaPorPrioridade().
        3) Retornar 0.

    Hipóteses:
        - Prioridade: 1 < 2 < 3 (menor valor = maior prioridade).
"""
def adicionarNaFila(fila, usuario):
    # PASSO 1: verificar se usuário já está na fila
    if consultarPosicaoNaFila(fila, usuario.login) != -1:
        # AS: usuário já existe, retorna erro
        return -1

    # PASSO 2: adicionar usuário no final da lista
    fila.append(usuario)

    # PASSO 3: reordenar por prioridade
    ordenarFilaPorPrioridade(fila)

    # AS: usuário adicionado com sucesso
    return 0

"""
    Nome: removerDaFila(fila, id_usuario)

    Objetivo:
        Retirar da fila o usuário cujo login == id_usuario.

    Acoplamento:
        - fila: list[Usuario].
        - id_usuario: str.
        - retorno: int — 0=removido, –1=não achou.

    Condições de Acoplamento:
        AE: fila pode estar vazia.
        AS: se achar, deleta elemento e devolve 0.

    Descrição:
        Percorre lista; ao encontrar .login igual, faz del fila[i].

    Hipóteses:
        - login é chave única na fila.
"""
def removerDaFila(fila, id_usuario):
    # PASSO 1: verificar se fila existe e não está vazia
    if not fila:
        return -1

    # PASSO 2: procurar e remover usuário da lista
    for i, usuario in enumerate(fila):
        if usuario.login == id_usuario:
            # PASSO 3: encontrou - remover da lista
            del fila[i]
            # AS: usuário removido com sucesso
            return 0

    # PASSO 4: usuário não encontrado
    return -1

"""
    Nome: ordenarFilaPorPrioridade(fila)

    Objetivo:
        Ordenar in-place pela prioridade (usuario.tipo):
        1 → primeiro, depois 2, depois 3; estabilidade preservada.

    Acoplamento:
        - fila: list[Usuario].
        - retorno: None (efeito colateral).

    Condições de Acoplamento:
        AE: fila inicializada.
        AS: ordem reposicionada conforme chave .tipo.

    Descrição:
        Usa list.sort(key=lambda u: u.tipo) — ordenação estável do Python garante
        manter ordem de chegada dentro de mesma prioridade.

    Hipóteses:
        - .tipo é int comparável.
"""
def ordenarFilaPorPrioridade(fila):
    # PASSO 1: verificar se há elementos para ordenar
    if not fila or len(fila) <= 1:
        return

    # PASSO 2: ordenar por tipo (prioridade) de forma estável
    # Menor tipo = maior prioridade
    # sort() é estável por padrão no Python
    fila.sort(key=lambda usuario: usuario.tipo)
    #! talvez exibir o estado da fila após cada operação de ordenação

    # AS: fila reordenada por prioridade mantendo estabilidade

"""
    Nome: retornaPrimeiro(fila)

    Objetivo:
        Obter o primeiro elemento sem removê-lo.

    Acoplamento:
        - fila: list[Usuario].
        - retorno: Usuario | None.

    Condições de Acoplamento:
        AE: fila inicializada.
        AS: None se vazia; caso contrário, fila[0].

    Descrição:
        Verifica fila; retorno direto de fila[0] se existir.

    Hipóteses:
        - Lista preserva ordem FIFO.
"""
def retornaPrimeiro(fila):
    # PASSO 1: verificar se fila existe e não está vazia
    if not fila:
        # AS: fila vazia, retorna None
        return None

    # PASSO 2: retornar primeiro elemento da lista sem remover
    # AS: retorna o objeto armazenado no primeiro elemento
    return fila[0]
