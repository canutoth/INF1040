"""
Nome: inicializarFila()

Objetivo: 
    Aloca e retorna uma nova estrutura de Fila inicializada.

Acoplamento:
    - Retorno: list — lista Python vazia para representar a fila.

Condições de Acoplamento:
    AE: Função chamada sem parâmetros.
    AS: Retorna uma lista vazia válida para representar o estado inicial da fila.

Descrição:
    1) Criar nova lista vazia.
    2) Retornar a lista criada.

Hipóteses:
    - A função é chamada uma vez no início do sistema.
    - Há memória suficiente para alocar a estrutura.

Restrições:
    - Deve ser chamada apenas uma vez por sessão do sistema.
"""


def inicializarFila():
    # PASSO 1: criar nova lista vazia
    fila = []
    # AS: fila inicializada como lista vazia
    return fila


"""
Nome: consultarPosicaoNaFila(fila, id_usuario)

Objetivo:
    Encontrar a posição de um usuário específico na fila de espera.

Acoplamento:
    - fila: list — lista Python representando a fila a ser consultada.
    - id_usuario: str — identificador único do usuário a ser procurado.
    - Retorno: int — posição do usuário (1, 2, 3...) ou -1 se não encontrado.

Condições de Acoplamento:
    AE: fila deve ser uma lista válida.
    AE: id_usuario deve ser string não vazia.
    AS: Retorna posição ordinal (base 1) se usuário encontrado.
    AS: Retorna -1 se usuário não está na fila.

Descrição:
    1) Receber fila e id_usuario.
    2) Percorrer a lista do início ao fim.
    3) Para cada usuário, comparar usuario.getLogin() com id_usuario.
    4) Se encontrar correspondência, retornar a posição atual (índice + 1).
    5) Se percorrer toda a fila sem encontrar, retornar -1.

Hipóteses:
    - O usuário é uma instância válida da classe Usuario com método getLogin().
    - O campo login do usuário é único e está preenchido.
    - A lista está íntegra.

Restrições:
    - Busca sequencial O(n) onde n é o tamanho da fila.
"""


def consultarPosicaoNaFila(fila, id_usuario):
    # PASSO 1: verificar se fila existe e não está vazia
    if not fila:
        return -1

    # PASSO 2: percorrer lista do início ao fim
    for i, usuario in enumerate(fila):
        # PASSO 3: comparar id do usuário atual com id_usuario procurado
        if usuario.getLogin() == id_usuario:
            # AS: usuário encontrado, retorna posição (base 1)
            return i + 1

    # PASSO 4: usuário não encontrado após percorrer toda a fila
    return -1


"""
Nome: adicionarNaFila(fila, usuario)

Objetivo:
    Inserir um usuário no final da fila de espera, evitando duplicatas e mantendo ordenação por prioridade.

Acoplamento:
    - fila: list — lista Python representando a fila onde inserir o usuário.
    - usuario: Usuario — objeto da classe Usuario representando o usuário.
    - Retorno: int — 0 se sucesso, -1 se usuário já está na fila.

Condições de Acoplamento:
    AE: fila deve ser uma lista válida.
    AE: usuario deve ser uma instância válida da classe Usuario com tipo em {1,2,3}.
    AS: Se usuário não está na fila, é inserido no final e fila é reordenada.
    AS: Após inserção, chama ordenarFilaPorPrioridade para reordenar.
    AS: Retorna 0 em caso de sucesso.

Descrição:
    1) Receber fila e usuario.
    2) Verificar se usuário já está na fila usando consultarPosicaoNaFila.
    3) Se já existe, retornar -1.
    4) Adicionar usuário no final da lista.
    5) Chamar ordenarFilaPorPrioridade.
    6) Retornar 0.

Hipóteses:
    - O usuário é uma instância válida da classe Usuario com métodos getLogin() e getTipo().
    - O usuário possui prioridade definida pelo tipo (1=INTERNO, 2=CONVIDADO, 3=EXTERNO).
    - A função ordenarFilaPorPrioridade está implementada corretamente.

Restrições:
    - Não permite usuários duplicados na fila.
"""


def adicionarNaFila(fila, usuario):
    # PASSO 1: verificar se usuário já está na fila
    if consultarPosicaoNaFila(fila, usuario.getLogin()) != -1:
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
    Remover um usuário específico da fila de espera.

Acoplamento:
    - fila: list — lista Python representando a fila de onde remover o usuário.
    - id_usuario: str — identificador do usuário a ser removido.
    - Retorno: int — 0 se sucesso, -1 se usuário não encontrado.

Condições de Acoplamento:
    AE: fila deve ser uma lista válida.
    AE: id_usuario deve ser string não vazia.
    AS: Se usuário encontrado, é removido da lista.
    AS: Retorna 0 em caso de sucesso, -1 se não encontrado.

Descrição:
    1) Receber fila e id_usuario.
    2) Percorrer a lista procurando o usuário.
    3) Se encontrado, remover da lista usando del ou remove.
    4) Retornar 0 se sucesso, -1 se não encontrado.

Hipóteses:
    - O usuário é uma instância válida da classe Usuario com método getLogin().
    - A lista está íntegra.
    - O usuário pode estar em qualquer posição da lista.

Restrições:
    - Operação O(n) devido à busca sequencial.
"""


def removerDaFila(fila, id_usuario):
    # PASSO 1: verificar se fila existe e não está vazia
    if not fila:
        return -1

    # PASSO 2: procurar e remover usuário da lista
    for i, usuario in enumerate(fila):
        if usuario.getLogin() == id_usuario:
            # PASSO 3: encontrou - remover da lista
            del fila[i]
            # AS: usuário removido com sucesso
            return 0

    # PASSO 4: usuário não encontrado
    return -1


"""
Nome: ordenarFilaPorPrioridade(fila)

Objetivo:
    Reordenar a fila segundo prioridade: menor valor de usuario.tipo primeiro, mantendo ordem de chegada para prioridades iguais.

Acoplamento:
    - fila: list — lista Python representando a fila a ser ordenada.
    - Retorno: None — função modifica a lista in-place.

Condições de Acoplamento:
    AE: fila deve ser uma lista válida.
    AS: Lista reordenada com usuários de menor tipo (maior prioridade) primeiro.
    AS: Para tipos iguais, mantém ordem de chegada original (estável).
    AS: Lista permanece íntegra após ordenação.

Descrição:
    1) Receber fila.
    2) Se fila vazia ou com 1 elemento, retornar sem alterações.
    3) Ordenar lista por tipo (prioridade) de forma estável usando sort().
    4) Lista é modificada in-place.

Hipóteses:
    - O usuário é uma instância válida da classe Usuario com método getTipo().
    - Tipo 1 (INTERNO) tem maior prioridade que tipo 2 (CONVIDADO) que tem maior que tipo 3 (EXTERNO).
    - A ordenação deve ser estável (preserva ordem original para elementos iguais).

Restrições:
    - Usa ordenação estável para preservar ordem de chegada em caso de empate.
"""


def ordenarFilaPorPrioridade(fila):
    # PASSO 1: verificar se há elementos para ordenar
    if not fila or len(fila) <= 1:
        return

    # PASSO 2: ordenar por tipo (prioridade) de forma estável
    # Menor tipo = maior prioridade
    # sort() é estável por padrão no Python
    fila.sort(key=lambda usuario: usuario.getTipo())

    # AS: fila reordenada por prioridade mantendo estabilidade


"""
Nome: retornaPrimeiro(fila)

Objetivo:
    Retornar o primeiro item da fila sem removê-lo, para consulta antes de operações de remoção.

Acoplamento:
    - fila: list — lista Python representando a fila a ser consultada.
    - Retorno: Object — objeto armazenado no primeiro elemento da fila, ou None se fila vazia.

Condições de Acoplamento:
    AE: fila deve ser uma lista válida.
    AS: Retorna o objeto armazenado no primeiro elemento se fila não vazia.
    AS: Retorna None se fila vazia.
    AS: Não modifica a lista.

Descrição:
    1) Receber fila.
    2) Verificar se fila existe e não está vazia.
    3) Se vazia, retornar None.
    4) Se não vazia, retornar o primeiro elemento da lista.

Hipóteses:
    - A lista está íntegra.
    - O primeiro elemento contém um objeto válido.

Restrições:
    - Operação O(1) - acesso direto ao primeiro elemento.
    - Não modifica a fila, apenas consulta.
    - Agnóstica ao tipo de objeto armazenado.
"""


def retornaPrimeiro(fila):
    # PASSO 1: verificar se fila existe e não está vazia
    if not fila:
        # AS: fila vazia, retorna None
        return None

    # PASSO 2: retornar primeiro elemento da lista sem remover
    # AS: retorna o objeto armazenado no primeiro elemento
    return fila[0]
