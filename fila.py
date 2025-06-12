class No:
    """Classe que representa um nó da lista encadeada da fila."""

    def __init__(self, usuario):
        self.usuario = usuario
        self.proximo = None


class Fila:
    """Estrutura da fila de espera."""

    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0


"""
Nome: inicializarFila()

Objetivo: 
    Aloca e retorna uma nova estrutura de Fila inicializada.

Acoplamento:
    - Retorno: Fila — objeto Fila inicializado com inicio=None, fim=None, tamanho=0.

Condições de Acoplamento:
    AE: Função chamada sem parâmetros.
    AS: Retorna uma instância válida de Fila com todos os campos inicializados em estado vazio.

Descrição:
    1) Criar nova instância da classe Fila.
    2) Inicializar inicio = None.
    3) Inicializar fim = None.
    4) Inicializar tamanho = 0.
    5) Retornar a instância criada.

Hipóteses:
    - A função é chamada uma vez no início do sistema.
    - Há memória suficiente para alocar a estrutura.

Restrições:
    - Deve ser chamada apenas uma vez por sessão do sistema.
"""


def inicializarFila():
    # PASSO 1: criar nova instância de Fila
    fila = Fila()
    # AS: fila inicializada com estado vazio (inicio=None, fim=None, tamanho=0)
    return fila


"""
Nome: consultarPosicaoNaFila(fila, id_usuario)

Objetivo:
    Encontrar a posição de um usuário específico na fila de espera.

Acoplamento:
    - fila: Fila — estrutura da fila a ser consultada.
    - id_usuario: str — identificador único do usuário a ser procurado.
    - Retorno: int — posição do usuário (1, 2, 3...) ou -1 se não encontrado.

Condições de Acoplamento:
    AE: fila deve ser uma instância válida de Fila.
    AE: id_usuario deve ser string não vazia.
    AS: Retorna posição ordinal (base 1) se usuário encontrado.
    AS: Retorna -1 se usuário não está na fila.

Descrição:
    1) Receber fila e id_usuario.
    2) Inicializar contador de posição = 1.
    3) Percorrer a fila do início ao fim.
    4) Para cada nó, comparar usuario.id com id_usuario.
    5) Se encontrar correspondência, retornar a posição atual.
    6) Se percorrer toda a fila sem encontrar, retornar -1.

Hipóteses:
    - O usuário é uma instância válida da classe Usuario com método getLogin().
    - O campo login do usuário é único e está preenchido.
    - A estrutura da fila está íntegra (ponteiros válidos).

Restrições:
    - Busca sequencial O(n) onde n é o tamanho da fila.
"""


def consultarPosicaoNaFila(fila, id_usuario):
    # PASSO 1: verificar se fila existe e não está vazia
    if not fila or fila.inicio is None:
        return -1

    # PASSO 2: percorrer fila do início ao fim
    posicao = 1
    no_atual = fila.inicio

    while no_atual is not None:
        # PASSO 3: comparar id do usuário atual com id_usuario procurado
        if no_atual.usuario.getLogin() == id_usuario:
            # AS: usuário encontrado, retorna posição
            return posicao

        # PASSO 4: avançar para próximo nó
        no_atual = no_atual.proximo
        posicao += 1

    # PASSO 5: usuário não encontrado após percorrer toda a fila
    return -1


"""
Nome: adicionarNaFila(fila, usuario)

Objetivo:
    Inserir um usuário no final da fila de espera, evitando duplicatas e mantendo ordenação por prioridade.

Acoplamento:
    - fila: Fila — estrutura da fila onde inserir o usuário.
    - usuario: Usuario — objeto da classe Usuario representando o usuário.
    - Retorno: int — 0 se sucesso, -1 se usuário já está na fila.

Condições de Acoplamento:
    AE: fila deve ser uma instância válida de Fila.
    AE: usuario deve ser uma instância válida da classe Usuario com tipo em {1,2,3}.
    AS: Se usuário não está na fila, é inserido no final e fila.tamanho é incrementado.
    AS: Após inserção, chama ordenarFilaPorPrioridade para reordenar.
    AS: Retorna 0 em caso de sucesso.

Descrição:
    1) Receber fila e usuario.
    2) Verificar se usuário já está na fila usando consultarPosicaoNaFila.
    3) Se já existe, retornar -1.
    4) Criar novo nó com o usuário.
    5) Inserir no final da fila (atualizar ponteiros).
    6) Incrementar fila.tamanho.
    7) Chamar ordenarFilaPorPrioridade.
    8) Retornar 0.

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

    # PASSO 2: criar novo nó
    novo_no = No(usuario)

    # PASSO 3: inserir no final da fila
    if fila.inicio is None:
        # Fila vazia
        fila.inicio = novo_no
        fila.fim = novo_no
    else:
        # Fila não vazia - adicionar no fim
        fila.fim.proximo = novo_no
        fila.fim = novo_no

    # PASSO 4: incrementar tamanho
    fila.tamanho += 1

    # PASSO 5: reordenar por prioridade
    ordenarFilaPorPrioridade(fila)

    # AS: usuário adicionado com sucesso
    return 0


"""
Nome: removerDaFila(fila, id_usuario)

Objetivo:
    Remover um usuário específico da fila de espera.

Acoplamento:
    - fila: Fila — estrutura da fila de onde remover o usuário.
    - id_usuario: str — identificador do usuário a ser removido.
    - Retorno: int — 0 se sucesso, -1 se usuário não encontrado.

Condições de Acoplamento:
    AE: fila deve ser uma instância válida de Fila.
    AE: id_usuario deve ser string não vazia.
    AS: Se usuário encontrado, é removido e fila.tamanho é decrementado.
    AS: Ponteiros da lista encadeada são atualizados corretamente.
    AS: Retorna 0 em caso de sucesso, -1 se não encontrado.

Descrição:
    1) Receber fila e id_usuario.
    2) Percorrer a fila procurando o usuário.
    3) Se encontrado, atualizar ponteiros para remover o nó.
    4) Tratar casos especiais (primeiro, último, meio da fila).
    5) Decrementar fila.tamanho.
    6) Retornar 0 se sucesso, -1 se não encontrado.

Hipóteses:
    - O usuário é uma instância válida da classe Usuario com método getLogin().
    - A estrutura da fila está íntegra.
    - O usuário pode estar em qualquer posição da fila.

Restrições:
    - Operação O(n) devido à busca sequencial.
"""


def removerDaFila(fila, id_usuario):
    # PASSO 1: verificar se fila existe e não está vazia
    if not fila or fila.inicio is None:
        return -1

    # PASSO 2: caso especial - remover primeiro elemento
    if fila.inicio.usuario.getLogin() == id_usuario:
        fila.inicio = fila.inicio.proximo
        if fila.inicio is None:
            # Era o único elemento
            fila.fim = None
        fila.tamanho -= 1
        return 0

    # PASSO 3: procurar elemento no meio ou fim da fila
    no_anterior = fila.inicio
    no_atual = fila.inicio.proximo

    while no_atual is not None:
        if no_atual.usuario.getLogin() == id_usuario:
            # PASSO 4: encontrou - atualizar ponteiros
            no_anterior.proximo = no_atual.proximo

            # Se era o último elemento, atualizar fim
            if no_atual == fila.fim:
                fila.fim = no_anterior

            fila.tamanho -= 1
            # AS: usuário removido com sucesso
            return 0

        # Avançar na busca
        no_anterior = no_atual
        no_atual = no_atual.proximo

    # PASSO 5: usuário não encontrado
    return -1


"""
Nome: ordenarFilaPorPrioridade(fila)

Objetivo:
    Reordenar a fila segundo prioridade: menor valor de usuario.tipo primeiro, mantendo ordem de chegada para prioridades iguais.

Acoplamento:
    - fila: Fila — estrutura da fila a ser ordenada.
    - Retorno: None — função modifica a fila in-place.

Condições de Acoplamento:
    AE: fila deve ser uma instância válida de Fila.
    AS: Fila reordenada com usuários de menor tipo (maior prioridade) primeiro.
    AS: Para tipos iguais, mantém ordem de chegada original (estável).
    AS: Estrutura da fila permanece íntegra após ordenação.

Descrição:
    1) Receber fila.
    2) Se fila vazia ou com 1 elemento, retornar sem alterações.
    3) Extrair todos os usuários da fila para uma lista.
    4) Ordenar lista por tipo (prioridade) de forma estável.
    5) Reconstruir a fila com os usuários ordenados.
    6) Atualizar ponteiros inicio, fim e manter tamanho.

Hipóteses:
    - O usuário é uma instância válida da classe Usuario com método getTipo().
    - Tipo 1 (INTERNO) tem maior prioridade que tipo 2 (CONVIDADO) que tem maior que tipo 3 (EXTERNO).
    - A ordenação deve ser estável (preserva ordem original para elementos iguais).

Restrições:
    - Usa ordenação estável para preservar ordem de chegada em caso de empate.
"""


def ordenarFilaPorPrioridade(fila):
    # PASSO 1: verificar se há elementos para ordenar
    if not fila or fila.tamanho <= 1:
        return

    # PASSO 2: extrair todos os usuários para uma lista
    usuarios = []
    no_atual = fila.inicio

    while no_atual is not None:
        usuarios.append(no_atual.usuario)
        no_atual = no_atual.proximo

    # PASSO 3: ordenar por tipo (prioridade) de forma estável
    # Menor tipo = maior prioridade
    usuarios.sort(key=lambda usuario: usuario.getTipo())

    # PASSO 4: reconstruir a fila com usuários ordenados
    fila.inicio = None
    fila.fim = None
    tamanho_original = fila.tamanho
    fila.tamanho = 0

    for usuario in usuarios:
        novo_no = No(usuario)

        if fila.inicio is None:
            # Primeiro elemento
            fila.inicio = novo_no
            fila.fim = novo_no
        else:
            # Adicionar no fim
            fila.fim.proximo = novo_no
            fila.fim = novo_no

        fila.tamanho += 1

    # AS: fila reordenada por prioridade mantendo estabilidade


"""
Nome: retornaPrimeiro(fila)

Objetivo:
    Retornar o primeiro item da fila sem removê-lo, para consulta antes de operações de remoção.

Acoplamento:
    - fila: Fila — estrutura da fila a ser consultada.
    - Retorno: Object — objeto armazenado no primeiro elemento da fila, ou None se fila vazia.

Condições de Acoplamento:
    AE: fila deve ser uma instância válida de Fila.
    AS: Retorna o objeto armazenado no primeiro elemento se fila não vazia.
    AS: Retorna None se fila vazia.
    AS: Não modifica a estrutura da fila.

Descrição:
    1) Receber fila.
    2) Verificar se fila existe e não está vazia.
    3) Se vazia, retornar None.
    4) Se não vazia, retornar o objeto armazenado no primeiro nó.

Hipóteses:
    - A estrutura da fila está íntegra (ponteiros válidos).
    - O primeiro elemento contém um objeto válido.

Restrições:
    - Operação O(1) - acesso direto ao primeiro elemento.
    - Não modifica a fila, apenas consulta.
    - Agnóstica ao tipo de objeto armazenado.
"""


def retornaPrimeiro(fila):
    # PASSO 1: verificar se fila existe e não está vazia
    if not fila or fila.inicio is None:
        # AS: fila vazia, retorna None
        return None

    # PASSO 2: retornar objeto armazenado no primeiro nó sem remover
    # AS: retorna o objeto armazenado no primeiro nó
    return fila.inicio.usuario
