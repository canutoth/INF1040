import csv
from vagas import Vaga

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
    def __init__(self, nome):
        self.nome = nome
        self.vagas = []  # Lista de objetos Vaga

    def adicionarVaga(self, vaga):
        self.vagas.append(vaga)

    def getVagaDisponivel(self):
        for vaga in self.vagas:
            if vaga.estaLivre():
                return vaga
        return None

    def buscarVagaPorLogin(self, login):
        for vaga in self.vagas:
            if vaga.estaOcupadaPor(login):
                return vaga
        return None

    def liberarVagaDe(self, usuario):
        vaga = self.buscarVagaPorLogin(usuario.login)
        if vaga:
            vaga.liberar()
            return vaga.id
        return None
    
    def ocuparVagaPorLogin(self, login):
        vaga = self.getVagaDisponivel()
        if vaga:
            sucesso = vaga.ocupar(login)
            return (True, vaga.id) if sucesso else (False, None)
        return (False, None)

    def vagas_livres(self):
        return sum(1 for vaga in self.vagas if vaga.estaLivre())

    def listarStatusVagas(self):
        print(f"\nStatus das vagas no {self.nome}:")
        for vaga in self.vagas:
            status_str = "Livre" if vaga.estaLivre() else f"Ocupada por {vaga.estado}"
            print(f"Vaga {vaga.id:02d}: {status_str}")
    
    def verificarStatusVaga(self, id_vaga):
        for vaga in self.vagas:
            if vaga.id == id_vaga:
                return vaga.status()
        return "ID de vaga inválido."
    
    def salvarEstadoEmCSV(self, writer):
         linha = [self.nome] + [vaga.estado if not vaga.estaLivre() else "0" for vaga in self.vagas]
         writer.writerow(linha)


def criarEstacionamentosDeCSV(caminho_csv):
    estacionamentos = []
    try:
        with open(caminho_csv, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row:
                    continue
                nome_estacionamento = row[0]
                vagas = []
                for i in range(1, len(row)):
                    try:
                        estado = row[i].strip()
                        vaga = Vaga(i)
                        if estado != "0":
                            vaga.ocupar(estado)
                        vagas.append(vaga)
                    except Exception:
                        continue
                est = Estacionamento(nome_estacionamento)
                for vaga in vagas:
                    est.adicionarVaga(vaga)
                estacionamentos.append(est)
    except FileNotFoundError:
        print(f"Arquivo {caminho_csv} não encontrado.")
    return estacionamentos

def getVagaDisponivel(est):
    vaga = est.getVagaDisponivel()
    return vaga.id if vaga else -1

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

def selecionarEstacionamento(estacionamentos):
    if not estacionamentos:
        print("⚠️ Nenhum estacionamento disponível.")
        return None
    while True:
        ListarEstacionamentos(estacionamentos)
        escolha = input("Escolha (número) › ").strip()
        if not escolha:
            return None
        try:
            op = int(escolha)
            return estacionamentos[op - 1]
        except (ValueError, IndexError):
            print("⚠️ Opção inválida. Tente novamente ou deixe vazio para cancelar.")

    
#XXX: ALTERAÇÕES DA SOFIA
#XXX: ALTERANDO PARA MELHORAR ACOPLAMENTO E ENCAPSULAMENTO
    # """Nome: _carregar_vagas()
    # Objetivo: carregar as vagas do estacionamento a partir de um arquivo CSV ou criar vagas padrão se o arquivo não existir.

    # Acoplamento:
    #     self.arquivo_vagas: str — caminho do arquivo CSV contendo os dados das vagas.
    #     self.vagas: list[tuple[int, str]] — lista de tuplas (id_vaga, status) armazenando as vagas carregadas ou criadas.

    # Condições de acoplamento:
    #     AE: self.arquivo_vagas é um caminho válido para leitura ou criação de arquivo.
    #     AS: retorna uma lista de tuplas (id_vaga, status) com as vagas carregadas ou criadas.

    # Descrição:
    #     1) Tenta abrir o arquivo CSV indicado por self.arquivo_vagas.
    #     2) Para cada linha válida (com pelo menos 2 colunas), converte o primeiro elemento para inteiro (id_vaga) e lê o segundo como string (status).
    #     3) Se o arquivo não for encontrado, cria 10 vagas padrão livres no formato (id_vaga, "0").
    #     4) Salva imediatamente as vagas padrão no arquivo.
    #     5) Retorna a lista de vagas.

    # Hipóteses:
    #     - O arquivo CSV (se existir) contém linhas no formato esperado (int, str).
    #     - O diretório onde o arquivo será criado ou lido possui permissão de leitura e escrita.
    # """
    # #TODO: não pode abrir .csv aqui, tem que criar uma variável que vai ser populada pelo principal.py
    # def _carregar_vagas(self):
    #     vagas = []
    #     try:
    #         with open(self.arquivo_vagas, newline='') as csvfile:
    #             reader = csv.reader(csvfile)
    #             for row in reader:
    #                 if len(row) >= 2:
    #                     id_vaga = int(row[0])
    #                     status = row[1]
    #                     vagas.append((id_vaga, status))
    #     except FileNotFoundError:
    #         print(f"Arquivo {self.arquivo_vagas} não encontrado. Criando vagas padrão.")
    #         vagas = [(i, "0") for i in range(10)]  # Exemplo: 10 vagas padrão
    #         self.vagas = vagas
    #         self.salvar_vagas()
    #     return vagas

    # #TODO: não pode abrir .csv aqui, tem que criar uma variável que vai ser populada pelo principal.py
    # """Nome: salvar_vagas()

    # Objetivo: persistir o estado atual das vagas no arquivo CSV.

    # Acoplamento:
    #     self.vagas: list[tuple[int, str]] — lista de vagas a serem salvas.
    #     self.arquivo_vagas: str — caminho do arquivo CSV de destino.

    # Condições de acoplamento:
    #     AE: self.vagas contém vagas válidas (int, str).
    #     AS: arquivo CSV atualizado com as vagas atuais.

    # Descrição:
    #     1) Abre o arquivo no modo escrita.
    #     2) Grava as vagas linha por linha no formato (id_vaga, status).
    #     3) Fecha o arquivo.

    # Hipóteses:
    #     - O arquivo pode ser aberto no modo escrita.
    # """
    # def salvar_vagas(self):
    #     with open(self.arquivo_vagas, mode='w', newline='') as csvfile:
    #         writer = csv.writer(csvfile)
    #         for id_vaga, status in self.vagas:
    #             writer.writerow([id_vaga, status])