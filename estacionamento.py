import csv

"""
Nome: Estacionamento(nome, arquivo_vagas)

Objetivo: criar e gerenciar um estacionamento com vagas lidas de um arquivo CSV.

Acoplamento:
    nome: str — nome do estacionamento.
    arquivo_vagas: str — caminho do arquivo CSV contendo dados das vagas.
    vagas: list[tuple[int, str]] — lista de tuplas (id_vaga, status).

Condições de acoplamento:
    AE: nome deve ser uma string não vazia.
    AE: arquivo_vagas deve ser um caminho válido ou um arquivo que poderá ser criado.
    AS: instancia o estacionamento com as vagas carregadas do arquivo.

Descrição:
    1) Inicializa o estacionamento com nome e arquivo.
    2) Carrega as vagas do arquivo CSV no formato (id_vaga, status).
    3) Se o arquivo não existir, cria vagas padrão (10 vagas livres).
    4) Salva o estado inicial das vagas no arquivo (se criado).

Hipóteses:
    - O arquivo CSV está acessível ou pode ser criado.
    - O diretório de execução possui permissão de leitura/escrita.

"""
class Estacionamento:
    def __init__(self, nome, arquivo_vagas):
        self.nome = nome
        self.arquivo_vagas = arquivo_vagas
        self.vagas = self._carregar_vagas()

    """Nome: _carregar_vagas()
    Objetivo: carregar as vagas do estacionamento a partir de um arquivo CSV ou criar vagas padrão se o arquivo não existir.

    Acoplamento:
        self.arquivo_vagas: str — caminho do arquivo CSV contendo os dados das vagas.
        self.vagas: list[tuple[int, str]] — lista de tuplas (id_vaga, status) armazenando as vagas carregadas ou criadas.

    Condições de acoplamento:
        AE: self.arquivo_vagas é um caminho válido para leitura ou criação de arquivo.
        AS: retorna uma lista de tuplas (id_vaga, status) com as vagas carregadas ou criadas.

    Descrição:
        1) Tenta abrir o arquivo CSV indicado por self.arquivo_vagas.
        2) Para cada linha válida (com pelo menos 2 colunas), converte o primeiro elemento para inteiro (id_vaga) e lê o segundo como string (status).
        3) Se o arquivo não for encontrado, cria 10 vagas padrão livres no formato (id_vaga, "0").
        4) Salva imediatamente as vagas padrão no arquivo.
        5) Retorna a lista de vagas.

    Hipóteses:
        - O arquivo CSV (se existir) contém linhas no formato esperado (int, str).
        - O diretório onde o arquivo será criado ou lido possui permissão de leitura e escrita.
    """
    #TODO: não pode abrir .csv aqui, tem que criar uma variável que vai ser populada pelo principal.py
    def _carregar_vagas(self):
        vagas = []
        try:
            with open(self.arquivo_vagas, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 2:
                        id_vaga = int(row[0])
                        status = row[1]
                        vagas.append((id_vaga, status))
        except FileNotFoundError:
            print(f"Arquivo {self.arquivo_vagas} não encontrado. Criando vagas padrão.")
            vagas = [(i, "0") for i in range(10)]  # Exemplo: 10 vagas padrão
            self.vagas = vagas
            self.salvar_vagas()
        return vagas

    #TODO: não pode abrir .csv aqui, tem que criar uma variável que vai ser populada pelo principal.py
    """Nome: salvar_vagas()

    Objetivo: persistir o estado atual das vagas no arquivo CSV.

    Acoplamento:
        self.vagas: list[tuple[int, str]] — lista de vagas a serem salvas.
        self.arquivo_vagas: str — caminho do arquivo CSV de destino.

    Condições de acoplamento:
        AE: self.vagas contém vagas válidas (int, str).
        AS: arquivo CSV atualizado com as vagas atuais.

    Descrição:
        1) Abre o arquivo no modo escrita.
        2) Grava as vagas linha por linha no formato (id_vaga, status).
        3) Fecha o arquivo.

    Hipóteses:
        - O arquivo pode ser aberto no modo escrita.
    """
    def salvar_vagas(self):
        with open(self.arquivo_vagas, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for id_vaga, status in self.vagas:
                writer.writerow([id_vaga, status])

    """Nome: vagas_livres()

    Objetivo: contar o número de vagas livres no estacionamento.

    Acoplamento:
        self.vagas: list[tuple[int, str]] — lista das vagas do estacionamento.

    Condições de acoplamento:
        AE: self.vagas contém (int, str).
        AS: retorna o número de vagas livres (status == "0").

    Descrição:
        1) Percorre a lista de vagas.
        2) Conta quantas têm status "0".
        3) Retorna o total.

    Hipóteses:
        - O estado das vagas está corretamente carregado na memória.
    """
    def vagas_livres(self):
        return sum(1 for _, status in self.vagas if status == "0")

    def get_vaga_disponivel(self):
        for id_vaga, status in self.vagas:
            if status == "0":
                return id_vaga
        return -1
    
    #TODO: funções de acesso para: ALOCAR, LIBERAR e GET(vaga ocupada pelo usuario atual)

#TODO: criar função de criar estacionamento (ex. inicializaFila, só q p est)
#TODO: criar função de acesso que recebe o que vem csv e crie uma lista de vagas pra todo estacionamento

"""
Nome: ListarEstacionamentos(estacionamentos)

Objetivo: listar os estacionamentos e o número de vagas livres em cada um.

Acoplamento:
    estacionamentos: list[Estacionamento] — lista de objetos Estacionamento.

Condições de acoplamento:
    AE: lista contém objetos válidos de Estacionamento.
    AS: exibe informações no terminal.

Descrição:
    1) Percorre a lista de estacionamentos.
    2) Exibe nome e número de vagas livres de cada um.

Hipóteses:
    - Os objetos possuem método vagas_livres funcional.
"""
def ListarEstacionamentos(estacionamentos):
    print("\nEstacionamentos disponíveis:")
    for idx, est in enumerate(estacionamentos, 1):
        print(f"{idx}. {est.nome} – Vagas livres: {est.vagas_livres()}")

#TODO: isso é necessário? acho q pode ser uma função interna da classe Estacionamento
"""
Nome: BuscarVagasDisponiveis(est)

Objetivo: exibir o status de todas as vagas de um estacionamento.

Acoplamento:
    est: Estacionamento — estacionamento a ser consultado.

Condições de acoplamento:
    AE: est é um objeto Estacionamento válido.
    AS: imprime no terminal o status das vagas.

Descrição:
    1) Percorre as vagas do estacionamento.
    2) Exibe se estão livres ou ocupadas e por quem.

Hipóteses:
    - O objeto Estacionamento está carregado corretamente.

"""
def BuscarVagasDisponiveis(est):
    print(f"\nStatus das vagas no {est.nome}:")
    for id_vaga, status in est.vagas:
        status_str = "Livre" if status == "0" else f"Ocupada por {status}"
        print(f"Vaga {id_vaga:02d}: {status_str}")

"""
Nome: getVagaDisponivel(est)

Objetivo: retornar o ID da primeira vaga livre de um estacionamento.

Acoplamento:
    est: Estacionamento — estacionamento a ser consultado.

Condições de acoplamento:
    AE: est é um objeto Estacionamento válido.
    AS: retorna ID da primeira vaga livre ou -1.

Descrição:
    1) Chama est.get_vaga_disponivel().
    2) Retorna o resultado.

Hipóteses:
    - O método do estacionamento está correto.

"""
def getVagaDisponivel(est):
    return est.get_vaga_disponivel()

def selecionarEstacionamento(estacionamentos):
    if not estacionamentos:
        return None
    print("\nEstacionamentos disponíveis:")
    ListarEstacionamentos(estacionamentos)
    try:
        op = int(input("Escolha (número) › "))
        return estacionamentos[op-1]
    except (ValueError, IndexError):
        return -1