# principal.py
# -----------------------------------------------------------------------------
# Módulo principal do sistema de gerenciamento de estacionamento
# -----------------------------------------------------------------------------
import csv
import sys
import usuario as usuario_mod
import login as login_mod
import fila        as fila_mod
import estacionamento as est_mod

# ---------------------------- variáveis globais ------------------------------
FILA                = None          # ponteiro para a fila principal
ESTACIONAMENTOS     = []            # lista de objetos/estruturas de estacionamento
USUARIO_ATUAL       = None          # objeto usuário com sessão ativa

# Mapa simples de erros para mensagens
ERROS = {
    "OPCAO_INVALIDA" : "Opção inválida!",
    "NAO_AUTENTICADO": "É preciso estar autenticado para realizar esta operação.",
    "AUTH_FAIL"      : "Login ou senha incorretos.",
    "SEM_VAGAS"      : "Não há vagas disponíveis neste momento – você foi colocado(a) na fila.",
    "VAGA_NAO_ENCONTRADA": "Vaga inexistente.",
}

# ------------------------------ rotinas chave -------------------------------
"""
    Nome: IniciarSistema()

    Objetivo:
        Carregar usuários, inicializar fila e estacionamentos antes de qualquer
        interação do usuário.

    Acoplamento:
        - arquivos 'users.csv', 'guests.csv', 'estacionamentos.csv'.
        - módulos: usuario_mod, fila_mod, est_mod.
        - retorna: None (altera variáveis globais).

    Condições de Acoplamento:
        AE: arquivos CSV podem existir ou não; funções de leitura tratam falta.
        AS: FILA recebe lista vazia; ESTACIONAMENTOS é populado; usuários,
            convidados e fila ficam em memória prontos para uso.

    Descrição:
        1) Carrega usuários recorrentes (tipo 1) e convidados (tipo 2).
        2) Cria FILA vazia via fila_mod.inicializarFila().
        3) Constrói objetos Estacionamento a partir do CSV de estado.
        4) Exibe mensagem de sucesso.

    Hipóteses:
        - Funções usuario_mod.carregarUsuarios e est_mod.criarEstacionamentosDeCSV
          estão implementadas corretamente.

    Restrições:
        - Deve ser chamada uma única vez, logo no início do programa.
"""
def IniciarSistema():
    global FILA, ESTACIONAMENTOS

    # 1. Carregar usuários e convidados
    usuario_mod.carregarUsuarios("users.csv")
    usuario_mod.carregarUsuarios("guests.csv", tipo_padrao=2)

    # 2. Fila
    FILA = fila_mod.inicializarFila()

    # 3. Estacionamentos 
    ESTACIONAMENTOS = est_mod.criarEstacionamentosDeCSV("estacionamentos.csv")

    print("✅ Sistema iniciado com sucesso.")

"""
    Nome: MenuInicial()

    Objetivo:
        Controlar a etapa de pré-login: autenticar usuário ou criar conta.

    Acoplamento:
        - leitura: input().
        - módulos: AutenticarUsuario, usuario_mod.criaInterno / criaConvidado.
        - variável global USUARIO_ATUAL (pode ser setada aqui).

    Condições de Acoplamento:
        AE: IniciarSistema() já executado.
        AS: Sai do loop somente quando USUARIO_ATUAL for definido ou o usuário
            escolher encerrar (opção 3).

    Descrição:
        Loop até USUARIO_ATUAL deixar de ser None:  
        1) Exibir menu (Login / Criar conta / Sair).  
        2) Delegar ações conforme escolha.  
        3) Em “Criar conta”, perguntar se é interna ou visitante.

    Hipóteses:
        - Criação de contas valida duplicidade e formato.

    Restrições:
        - Uso de input síncrono; sem timeout.
"""
def MenuInicial():
    global USUARIO_ATUAL
    while USUARIO_ATUAL is None:
        print("\n======  BEM-VINDO(A)  ======")
        print("1) Login")
        print("2) Criar conta")
        print("3) Sair")
        escolha = input("Escolha › ").strip()

        if escolha == "1":
            AutenticarUsuario()
        elif escolha == "2":
            print("\nVocê deseja criar uma conta como:")
            print("1) Aluno, Professor ou Funcionário")
            print("2) Visitante")
            tipo = input("Escolha › ").strip()
            if tipo == "1":
                usuario_mod.criaInterno()
            elif tipo == "2":
                usuario_mod.criaConvidado()
            else:
                TratarErros("OPCAO_INVALIDA")
        elif escolha == "3":
            EncerrarSistema()
        else:
            TratarErros("OPCAO_INVALIDA")


"""
    Nome: ExibirMenuPrincipal()

    Objetivo:
        Oferecer ao usuário autenticado as operações principais:
        alocar vaga, liberar vaga, ver resumo ou encerrar.

    Acoplamento:
        - leitura: input().
        - funções: AlocarVaga, LiberarVaga, ExibirResumo, EncerrarSistema.

    Condições de Acoplamento:
        AE: USUARIO_ATUAL definido.
        AS: Mantém loop até EncerrarSistema() disparar sys.exit().

    Descrição:
        Constrói dicionário {opção: função}.  
        Mostra menu, lê escolha, despacha para a rotina adequada ou exibe erro.

    Hipóteses:
        - USUARIO_ATUAL continuará válido durante a sessão.

    Restrições:
        - Bloco infinito; ideal para CLI interativo.
    """
def ExibirMenuPrincipal():
    opcoes = {
        "1": AlocarVaga,
        "2": LiberarVaga,
        "3": ExibirResumo,
        "4": EncerrarSistema
    }
    while True:
        print("\n======  MENU PRINCIPAL  ======")
        print("1) Alocar vaga")
        print("2) Liberar vaga")
        print("3) Exibir resumo")
        print("4) Sair")
        escolha = input("Escolha › ").strip()

        acao = opcoes.get(escolha)
        if acao:
            acao()
        else:
            TratarErros("OPCAO_INVALIDA")

"""
    Nome: AutenticarUsuario()

    Objetivo:
        Solicitar credenciais e definir USUARIO_ATUAL quando válidas.

    Acoplamento:
        - login_mod.autentica().
        - usuario_mod.listarUsuarios() – lista de objetos Usuario.
        - variável global USUARIO_ATUAL.

    Condições de Acoplamento:
        AE: lista de usuários carregada.
        AS: USUARIO_ATUAL recebe objeto Usuario se sucesso; caso contrário
            exibe erro apropriado.

    Descrição:
        1) Ler login e senha.  
        2) Chamar login_mod.autentica().  
        3) Se retorno não-None → setar USUARIO_ATUAL.  
        4) Caso contrário → TratarErros("AUTH_FAIL").

    Hipóteses:
        - Função autentica devolve objeto ou None, não lança exceção.
    """
def AutenticarUsuario():
    global USUARIO_ATUAL
    login_inp = input("Login › ").strip()
    senha_inp = input("Senha › ").strip()

    usuario = login_mod.autentica(login_inp, senha_inp, usuario_mod.listarUsuarios())
    if usuario:
        USUARIO_ATUAL = usuario
        print(f"✅ Bem-vindo(a), {USUARIO_ATUAL.login}!")
    else:
        TratarErros("AUTH_FAIL")

"""
    Nome: AlocarVaga()

    Objetivo:
        Tentar ocupar uma vaga livre para USUARIO_ATUAL ou colocá-lo na FILA.

    Acoplamento:
        - est_mod.selecionarEstacionamento(), est_mod.getVagaDisponivel().
        - Estacionamento.ocuparVagaPorLogin().
        - fila_mod.* para gerenciamento de fila.

    Condições de Acoplamento:
        AE: USUARIO_ATUAL != None.
        AS: Vaga ocupada ou usuário inserido na FILA.

    Descrição:
        1) Verifica autenticação.  
        2) Permite escolha do estacionamento.  
        3) Se getVagaDisponivel == –1 → GerenciaFila + erro “SEM_VAGAS”.  
        4) Caso contrário → ocuparVagaPorLogin() e confirmar.

    Hipóteses:
        - ocuparVagaPorLogin() devolve tupla(sucesso,id); usamos apenas efeito.
    """
def AlocarVaga():
    if USUARIO_ATUAL is None:
        TratarErros("NAO_AUTENTICADO")
        return

    est = est_mod.selecionarEstacionamento(ESTACIONAMENTOS)
    if est == -1:
        TratarErros("OPCAO_INVALIDA")
    if not est:
        print("Nenhum estacionamento selecionado para alocar vaga")
        return
    
    vaga_disp = est_mod.getVagaDisponivel(est)
    if vaga_disp == -1:
        GerenciaFila(USUARIO_ATUAL)
        TratarErros("SEM_VAGAS")
    else:
        est.ocuparVagaPorLogin(USUARIO_ATUAL.login)
        print(f"✅ Vaga {vaga_disp} ocupada. Boa estadia!")

"""
    Nome: LiberarVaga()

    Objetivo:
        Liberar a vaga ocupada por USUARIO_ATUAL (qualquer estacionamento).

    Acoplamento:
        - Estacionamento.liberarVagaDe().
        - AtualizarEstado() para realocar fila.

    Condições de Acoplamento:
        AE: USUARIO_ATUAL autentica-do.
        AS: Vaga liberada ou erro VAGA_NAO_ENCONTRADA.

    Descrição:
        Itera todos os estacionamentos:  
        • se liberarVagaDe() devolver id → imprime sucesso e chama
          AtualizarEstado(est).  
        • se nenhum estacionamento contiver o usuário → erro.

    Hipóteses:
        - Cada usuário ocupa no máximo uma vaga.
    """
def LiberarVaga():
    if USUARIO_ATUAL is None:
        TratarErros("NAO_AUTENTICADO")
        return

    for est in ESTACIONAMENTOS:
        vaga_id = est.liberarVagaDe(USUARIO_ATUAL)
        if vaga_id is not None:
            print(f"✅ Vaga {vaga_id} liberada no estacionamento '{est.nome}'.")
            AtualizarEstado(est)
            return

    TratarErros("VAGA_NAO_ENCONTRADA")

"""
    Nome: GerenciaFila(usuario)

    Objetivo:
        Garantir que `usuario` esteja na FILA exatamente uma vez, ordenada
        por prioridade (.tipo).

    Acoplamento:
        - fila_mod.consultarPosicaoNaFila, adicionarNaFila, ordenarFilaPorPrioridade.
        - variável global FILA.

    Condições de Acoplamento:
        AE: FILA inicializada.
        AS: FILA contém usuário e está ordenada.

    Descrição:
        Se consultarPosicaoNaFila == –1 → adicionarNaFila(); depois reordena.

    Hipóteses:
        - Prioridade: tipo 1 < 2 < 3.
    """
def GerenciaFila(usuario):
    if fila_mod.consultarPosicaoNaFila(FILA, usuario) == -1:
        fila_mod.adicionarNaFila(FILA, usuario)
        fila_mod.ordenarFilaPorPrioridade(FILA)

"""
    Nome: AtualizarEstado(est)

    Objetivo:
        Após liberação de vaga, chamar o primeiro da FILA (se houver).

    Acoplamento:
        - est: Estacionamento onde surgiu vaga.
        - est.getVagaDisponivel() / ocuparVagaPorLogin().
        - fila_mod.retornaPrimeiro / removerDaFila.

    Condições de Acoplamento:
        AE: est válido; FILA inicializada.
        AS: Se vaga livre e fila não vazia → ocupação + remoção da FILA.

    Descrição:
        1) Verificar vaga livre.  
        2) Se existir, pegar primeiro da FILA.  
        3) Tentar ocupar; se sucesso → removerDaFila + mensagem.

    Hipóteses:
        - ocuparVagaPorLogin() retorna (sucesso, id).
    """
def AtualizarEstado(est):
    vaga = est.getVagaDisponivel
    if not vaga:
        return

    # há vaga livre – verificar fila
    prox = fila_mod.retornaPrimeiro(FILA)  
    if prox is not None:
        sucesso = est.ocuparVagaPorLogin(prox.login)
        if sucesso:
            fila_mod.removerDaFila(FILA, prox)
            print(f"🔔 Usuário {prox.login} foi chamado para ocupar a vaga {vaga}.")

"""
    Nome: ExibirResumo()

    Objetivo:
        Apresentar visão geral do sistema: vagas por estacionamento, tamanho da
        FILA e usuário autenticado.

    Acoplamento:
        - est_mod.ListarEstacionamentos().
        - FILA global (.tamanho) e USUARIO_ATUAL.

    Descrição:
        1) Delegar listagem de vagas a est_mod.  
        2) Exibir tamanho da fila.  
        3) Mostrar login do usuário autenticado (ou “Nenhum”).

    Restrições:
        - Apenas saída para console; não altera estado.
    """
def ExibirResumo():
    print("\n=======  RESUMO DO SISTEMA  =======")
    est_mod.ListarEstacionamentos(ESTACIONAMENTOS)

    tamanho_fila = FILA.tamanho if FILA else 0
    print(f"Usuários na fila: {tamanho_fila}")
    if USUARIO_ATUAL:
        print(f"Usuário autenticado: {USUARIO_ATUAL.login}")
    else:
        print("Nenhum usuário autenticado.")

"""
    Nome: EncerrarSistema()

    Objetivo:
        Persistir usuários, convidados e estado dos estacionamentos em CSV, e
        então encerrar o programa.

    Acoplamento:
        - usuario_mod.salvarUsuarios().
        - Estacionamento.salvarEstadoEmCSV() em loop de ESTACIONAMENTOS.
        - sys.exit(0).

    Descrição:
        1) Salvar users.csv e guests.csv via usuario_mod.  
        2) Abrir estacionamentos.csv e gravar o snapshot de cada estacionamento.  
        3) Imprimir confirmação e sair.

    Restrições:
        - Chama sys.exit(), portanto não retorna.
    """
def EncerrarSistema():
    usuario_mod.salvarUsuarios("users.csv", "guests.csv")
    with open("estacionamentos.csv", mode="w", newline='', encoding="utf-8") as f:
       writer = csv.writer(f)
       for est in ESTACIONAMENTOS:
          est.salvarEstadoEmCSV(writer)

    print("✔️  Dados salvos. Até logo!")
    sys.exit(0)

"""
    Nome: TratarErros(codigo)

    Objetivo:
        Imprimir mensagem de erro amigável correspondente ao código.

    Acoplamento:
        - ERROS: dict.

    Descrição:
        Faz lookup em ERROS e imprime resultado (default “Erro desconhecido.”).
    """
def TratarErros(codigo):
    print(f"⚠️  {ERROS.get(codigo, 'Erro desconhecido.')}")

# --------------------------- execução direta ---------------------------------
if __name__ == "__main__":
    IniciarSistema()
    MenuInicial()
    ExibirMenuPrincipal()

# # ---------------------------- utilidades internas ----------------------------
# """
#     Nome: _carregar_csv(caminho)

#     Objetivo:
#        - Ler um arquivo .csv delimitado por ‘;’ e convertê-lo em lista de tuplas.

#     Acoplamento:
#        - caminho: str — path para o arquivo .csv.
#        - retorno: list[tuple[str, str, int]] — cada tupla → (login, senha, tipo).

#     Condições de Acoplamento:
#        AE: caminho deve apontar para um arquivo .csv válido ou inexistente.
#        AS: Caso o arquivo exista, retorna estrutura list[...] com os registros lidos.
#        AS: Se o arquivo não existir, retorna lista vazia (primeira execução).

#     Descrição:
#        1) Tentar abrir o arquivo no modo leitura, encoding UTF-8.
#        2) Iterar sobre csv.reader(), convertendo cada linha não vazia
#           em (login, senha, int(tipo)).
#        3) Em FileNotFoundError, capturar exceção e retornar [].

#     Hipóteses:
#        - Arquivo, se existir, está formatado como “login;senha;tipo”.

#     Restrições:
#        - Não cria nem modifica arquivos; somente leitura.
#     """
# def _carregar_csv(caminho, tipo_padrao=None):
#     try:
#         with open(caminho, newline='', encoding="utf-8") as f:
#             reader = csv.reader(f, delimiter=',')
#             for row in reader:
#                 if not row:
#                     continue  # ignora linhas completamente vazias
#                 login = row[0].strip() if len(row) > 0 else ""
#                 senha = row[1].strip() if len(row) > 1 else ""
#                 try:
#                     tipo = int(row[2]) if len(row) > 2 else tipo_padrao
#                 except ValueError:
#                     tipo = tipo_padrao  # ignora erro de conversão e usa padrão

#                 if login and senha and tipo is not None:
#                     #TODO: isso rompe com o encapsulamento?
#                     usuario_mod.criaInterno(login, senha)
#     except FileNotFoundError:
#         pass

# """
#     Nome: _salvar_csv(caminho, dados)

#     Objetivo:
#        - Persistir em disco a lista de tuplas recebida, no formato CSV ‘;’.

#     Acoplamento:
#        - caminho: str — destino do arquivo .csv.
#        - dados: list[tuple] — estrutura já validada a ser gravada.
#        - retorno: None.

#     Condições de Acoplamento:
#        AE: dados deve ser iterável contendo sub-iteráveis (tuplas ou listas).
#        AS: Arquivo é sobrescrito/ criado com conteúdo de dados.

#     Descrição:
#        1) Abrir (ou criar) o arquivo no modo escrita, encoding UTF-8.
#        2) Utilizar csv.writer(delimiter=';') para gravar cada tupla.

#     Hipóteses:
#        - Permissões de escrita no diretório estão concedidas.

#     Restrições:
#        - Sobrescreve totalmente o arquivo; não há append incremental.
#     """
# def _salvar_csv(caminho, dados):
#     #TODO: pensar em nova forma de atualizar, sem romper com o encapsulamento, agora que usuarios é lista de Usuario
#     with open(caminho, "w", newline='', encoding="utf-8") as f:
#         writer = csv.writer(f, delimiter=',')
#         writer.writerows(dados)
