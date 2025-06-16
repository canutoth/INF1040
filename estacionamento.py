import csv
from vagas import Vaga

"""
    Nome: Estacionamento(nome)

    Objetivo:
       - Representar um estacionamento composto por objetos Vaga e fornecer
         operações de consulta, alocação e liberação de vagas.

    Acoplamento:
       - nome: str — nome identificador do estacionamento.
       - vagas: list[Vaga] — lista interna de vagas associadas (objeto Vaga).

    Condições de Acoplamento:
       AE: 'nome' deve ser string não vazia.
       AS: objeto instanciado com lista 'vagas' inicialmente vazia.

    Descrição:
       1) Atribui 'nome' ao atributo homônimo.
       2) Inicializa self.vagas como lista vazia.
       3) Vagas podem ser adicionadas via adicionarVaga() após a criação.

    Hipóteses:
       - Classe Vaga implementa id, ocupar(), liberar(), estaLivre(),
         estaOcupadaPor() e status().

    Restrições:
       - Operações dependem da correta implementação da classe Vaga.
"""
class Estacionamento:
    def __init__(self, nome):
        self.nome = nome
        self.vagas = []  # Lista de objetos Vaga

    """
        Nome: adicionarVaga(vaga)

        Objetivo:
           - Anexar nova vaga ao estacionamento.

        Acoplamento:
           - vaga: Vaga — instância a ser inserida.
           - retorno: None.

        Condições de Acoplamento:
           AE: 'vaga' é instância válida de Vaga.
           AS: vaga armazenada em self.vagas.

        Descrição:
           1) Executa append(self.vagas, vaga).

        Hipóteses:
           - Identificador de vaga (id) é único dentro do estacionamento.

        Restrições:
           - Não verifica duplicidade; responsabilidade do chamador.
    """
    def adicionarVaga(self, vaga):
        self.vagas.append(vaga)

    """
        Nome: getVagaDisponivel()

        Objetivo:
           - Obter a primeira vaga livre.

        Acoplamento:
           - retorno: Vaga ou None (quando não há vagas livres).

        Condições de Acoplamento:
           AE: self.vagas inicializada.
           AS: devolve instância cuja estaLivre() == True ou None.

        Descrição:
           1) Itera sobre self.vagas.
           2) Retorna a primeira cujo estado seja livre.

        Hipóteses:
           - estaLivre() implementada na classe Vaga.

        Restrições:
           - Critério “primeira” é a ordem da lista; sem priorização.
    """
    def getVagaDisponivel(self):
        for vaga in self.vagas:
            if vaga.estaLivre():
                return vaga
        return None

    """
        Nome: buscarVagaPorLogin(login)

        Objetivo:
           - Localizar a vaga ocupada por determinado usuário.

        Acoplamento:
           - login: str — identificador do usuário.
           - retorno: Vaga ou None.

        Condições de Acoplamento:
           AE: login string não vazia.
           AS: devolve vaga cuja estaOcupadaPor(login) == True ou None.

        Descrição:
           1) Percorre self.vagas.
           2) Retorna a vaga ocupada por 'login'.

        Hipóteses:
           - estaOcupadaPor(login) implementada em Vaga.

        Restrições:
           - Assumimos máximo de uma vaga por usuário.
    """
    def buscarVagaPorLogin(self, login):
        for vaga in self.vagas:
            if vaga.estaOcupadaPor(login):
                return vaga
        return None

    """
        Nome: liberarVagaDe(usuario)

        Objetivo:
           - Liberar a vaga atualmente ocupada por 'usuario'.

        Acoplamento:
           - usuario: objeto que possui atributo .login.
           - retorno: int (id da vaga liberada) ou None se não encontrada.

        Condições de Acoplamento:
           AE: usuario não nulo e possui .login.
           AS: vaga correspondente volta a estado livre.

        Descrição:
           1) Busca vaga via buscarVagaPorLogin().
           2) Se existir, chama vaga.liberar() e retorna vaga.id.

        Hipóteses:
           - Método liberar() redefine estado para livre.

        Restrições:
           - Nenhuma exceção lançada; retorna None se nada a liberar.
    """
    def liberarVagaDe(self, usuario):
        vaga = self.buscarVagaPorLogin(usuario.login)
        if vaga:
            vaga.liberar()
            return vaga.id
        return None
    
    """
        Nome: ocuparVagaPorLogin(login)

        Objetivo:
           - Ocupar a primeira vaga livre para o usuário 'login'.

        Acoplamento:
           - login: str — identificador do usuário.
           - retorno: (sucesso: bool, id_vaga: int|None).

        Condições de Acoplamento:
           AE: login string não vazia.
           AS: Ao sucesso, vaga marcada ocupada e id retornado.

        Descrição:
           1) Obter vaga livre via getVagaDisponivel().
           2) Se existir → vaga.ocupar(login).
              - se ocupar() True → (True, id)
              - else (falha)     → (False, None)
           3) Se inexistente → (False, None).

        Hipóteses:
           - ocupar(login) retorna bool de sucesso.

        Restrições:
           - Não há tentativa de reserva priorizada.
    """
    def ocuparVagaPorLogin(self, login):
        vaga = self.getVagaDisponivel()
        if vaga:
            sucesso = vaga.ocupar(login)
            return (True, vaga.id) if sucesso else (False, None)
        return (False, None)
    
    """
        Nome: vagas_livres()

        Objetivo:
           - Contar quantas vagas estão livres.

        Acoplamento:
           - retorno: int.

        Condições de Acoplamento:
           AE: self.vagas inicializada.
           AS: retorna quantidade de vagas com estaLivre() == True.

        Descrição:
           1) Usa expressão geradora + sum().

        Hipóteses:
           - Lista de vagas pode ser vazia.

        Restrições:
           - Complexidade O(n).
    """
    def vagas_livres(self):
        return sum(1 for vaga in self.vagas if vaga.estaLivre())

    """
        Nome: listarStatusVagas()

        Objetivo:
           - Exibir no console o estado de cada vaga.

        Acoplamento:
           - retorno: None (efeito colateral: print()).

        Condições de Acoplamento:
           AE: self.vagas inicializada.
           AS: Imprime “Livre” ou “Ocupada por <login>” para cada vaga.

        Descrição:
           1) Percorre self.vagas.
           2) Monta string de status e imprime formatada.

        Hipóteses:
           - Ambiente de execução possui stdout.

        Restrições:
           - Apenas uso interativo; não retorna estrutura de dados.
    """
    def listarStatusVagas(self):
        print(f"\nStatus das vagas no {self.nome}:")
        for vaga in self.vagas:
            status_str = "Livre" if vaga.estaLivre() else f"Ocupada por {vaga.estado}"
            print(f"Vaga {vaga.id:02d}: {status_str}")
    
    """
        Nome: verificarStatusVaga(id_vaga)

        Objetivo:
           - Obter status textual de uma vaga específica.

        Acoplamento:
           - id_vaga: int — identificador da vaga.
           - retorno: str — “Livre”, “Ocupada por <login>” ou erro.

        Condições de Acoplamento:
           AE: id_vaga inteiro positivo.
           AS: retorna string descritiva ou “ID de vaga inválido.”.

        Descrição:
           1) Procura vaga na lista pela comparação de id.
           2) Se encontrada → retorna vaga.status(); senão mensagem de erro.

        Hipóteses:
           - Método status() existe em Vaga.

        Restrições:
           - Não lança exceções.
    """
    def verificarStatusVaga(self, id_vaga):
        for vaga in self.vagas:
            if vaga.id == id_vaga:
                return vaga.status()
        return "ID de vaga inválido."
    
    """
        Nome: salvarEstadoEmCSV(writer)

        Objetivo:
           - Gravar linha no CSV contendo nome + estado de cada vaga.

        Acoplamento:
           - writer: csv.writer — instância já aberta para escrita.
           - retorno: None.

        Condições de Acoplamento:
           AE: writer aberto e configurado.
           AS: linha gravada no formato [nome, estado1, estado2, ...].

        Descrição:
           1) Constrói lista: [self.nome] + lista estados.
              - estado = login se ocupada, “0” se livre.
           2) writer.writerow(linha).

        Hipóteses:
           - Vagas possuem atributo .estado (login ou None).

        Restrições:
           - Não salva header; responsabilidade externa se necessário.
    """
    def salvarEstadoEmCSV(self, writer):
        linha = [self.nome] + [vaga.estado if not vaga.estaLivre() else "0" for vaga in self.vagas]
        writer.writerow(linha)

"""
    Nome: criarEstacionamentosDeCSV(caminho_csv)

    Objetivo:
       - Carregar múltiplos estacionamentos e seus estados de um arquivo CSV.

    Acoplamento:
       - caminho_csv: str — path para CSV no formato:
           nome_est,login_vaga1,login_vaga2,...
           (zero “0” indica vaga livre)
       - retorno: list[Estacionamento].

    Condições de Acoplamento:
       AE: arquivo deve existir e ser legível (ou FileNotFoundError tratado).
       AS: lista de Estacionamento com vagas corretamente ocupadas.

    Descrição:
       1) Abrir CSV e iterar linhas.
       2) Para cada linha:
          a. Criar Estacionamento(nome).
          b. Para cada coluna de estado → criar Vaga(i) e ocupar se login != "0".
       3) Retornar lista preenchida.

    Hipóteses:
       - IDs das vagas são dados pela ordem das colunas (1…n).

    Restrições:
       - Ignora colunas vazias ou erros de conversão silenciosamente.
"""
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

"""
    Nome: getVagaDisponivel(est)

    Objetivo:
       - Interface simples para retornar o ID da vaga livre (ou -1).

    Acoplamento:
       - est: Estacionamento.
       - retorno: int (id_vaga) ou -1 se indisponível.

    Condições de Acoplamento:
       AE: est instância válida.
       AS: inteiro retornado.

    Descrição:
       1) Chama est.getVagaDisponivel().
       2) Se None → -1; senão → vaga.id.

    Hipóteses:
       - Método getVagaDisponivel implementado conforme contrato.

    Restrições:
       - Função utilitária; não altera estado.
"""
def getVagaDisponivel(est):
    vaga = est.getVagaDisponivel()
    return vaga.id if vaga else -1

"""
    Nome: ListarEstacionamentos(estacionamentos)

    Objetivo:
       - Exibir no terminal nome e vagas livres de cada estacionamento.

    Acoplamento:
       - estacionamentos: list[Estacionamento].
       - retorno: None (efeito colateral: print()).

    Condições de Acoplamento:
       AE: lista contém objetos Estacionamento.
       AS: informação impressa no console.

    Descrição:
       1) Itera enumerate(estacionamentos, 1).
       2) Imprime índice, nome e est.vagas_livres().

    Hipóteses:
       - Método vagas_livres funciona.

    Restrições:
       - Uso meramente informativo; não retorna dados.
"""
def ListarEstacionamentos(estacionamentos):
    print("\nEstacionamentos disponíveis:")
    for idx, est in enumerate(estacionamentos, 1):
        print(f"{idx}. {est.nome} – Vagas livres: {est.vagas_livres()}")

"""
    Nome: selecionarEstacionamento(estacionamentos)

    Objetivo:
       - Permitir que o usuário escolha um estacionamento por índice.

    Acoplamento:
       - estacionamentos: list[Estacionamento].
       - input() para leitura do número.
       - retorno: Estacionamento escolhido ou None (cancelado/erro).

    Condições de Acoplamento:
       AE: lista pode estar vazia (trata caso).
       AS: devolve instância correspondente ou None.

    Descrição:
       1) Se vazio → avisa e retorna None.
       2) Loop mostra lista via ListarEstacionamentos().
       3) Lê escolha; vazio → cancela.
       4) Converte para int; trata ValueError/IndexError → repete.

    Hipóteses:
       - Ambiente permite leitura de stdin.

    Restrições:
       - Fica em loop até entrada válida ou cancelamento.
"""
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