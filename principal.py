# principal.py
# -----------------------------------------------------------------------------
# Módulo principal do sistema de gerenciamento de estacionamento
# -----------------------------------------------------------------------------
import csv
import sys
import usuario as usuario_mod
import fila as fila_mod
import estacionamento as est_mod

# ---------------------------- variáveis globais ------------------------------
ESTACIONAMENTOS = []
USUARIO_ATUAL = None

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
        Carregar usuários e estacionamentos antes de qualquer
        interação do usuário.

    Acoplamento:
        - arquivos 'users.csv', 'guests.csv', 'estacionamentos.csv'.
        - módulos: usuario_mod, est_mod.
        - retorna: None (altera variáveis globais).

    Condições de Acoplamento:
        AE: arquivos CSV podem existir ou não; funções de leitura tratam falta.
        AS: ESTACIONAMENTOS é populado; usuários e convidados ficam em memória
            prontos para uso.

    Descrição:
        1) Carrega usuários recorrentes (tipo 1) e convidados (tipo 2).
        2) Constrói objetos Estacionamento a partir do CSV de estado.
        3) Exibe mensagem de sucesso.

    Hipóteses:
        - Funções usuario_mod.carregarUsuarios e est_mod.criarEstacionamentosDeCSV
          estão implementadas corretamente.

    Restrições:
        - Deve ser chamada uma única vez, logo no início do programa.
"""
def IniciarSistema():
    global ESTACIONAMENTOS

    # 1. Carregar usuários e convidados
    usuario_mod.carregarUsuarios("users.csv")
    usuario_mod.carregarUsuarios("guests.csv", tipo_padrao=2)

    # 2. Estacionamentos 
    ESTACIONAMENTOS = est_mod.criar_estacionamentos_de_csv("estacionamentos.csv")

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
            print("2) Convidado")
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
    - usuario_mod.autentica(login, senha) — devolve:
        • dict do usuário (sucesso)
        • 1 = login inexistente
        • 2 = senha incorreta
        • 3 = campos vazios
    - variável global USUARIO_ATUAL.

Descrição:
    1) Ler login e senha do teclado.
    2) Chamar usuario_mod.autentica().
    3) Se retornar dict → armazenar em USUARIO_ATUAL e saudar usuário.
    4) Se retornar código de erro → imprimir mensagem específica.
"""
def AutenticarUsuario():
    global USUARIO_ATUAL
    login_inp = input("Login › ").strip()
    senha_inp = input("Senha › ").strip()

    resultado = usuario_mod.autentica(login_inp, senha_inp)
    if isinstance(resultado, dict):  # Sucesso - retornou o usuário
        USUARIO_ATUAL = resultado
        print(f"✅ Bem-vindo(a), {usuario_mod.getLogin(USUARIO_ATUAL)}!")
    else:  # Erro - retornou código numérico
        if resultado == 1:
            print("⚠️ Login inexistente.")
        elif resultado == 2:
            print("⚠️ Senha incorreta.")
        elif resultado == 3:
            print("⚠️ Campos inválidos. Login e senha devem ser preenchidos.")
        else:
            TratarErros("AUTH_FAIL")

"""
    Nome: AlocarVaga()

    Objetivo:
        Tentar ocupar uma vaga livre para USUARIO_ATUAL ou colocá-lo na FILA.

    Acoplamento:
        - est_mod.selecionarEstacionamento(), est_mod.get_vaga_disponivel().
        - Estacionamento.ocupar_vaga_por_login().
        - fila_mod.* para gerenciamento de fila.

    Condições de Acoplamento:
        AE: USUARIO_ATUAL != None.
        AS: Vaga ocupada ou usuário inserido na FILA.

    Descrição:
        1) Verifica autenticação.  
        2) Permite escolha do estacionamento.  
        3) Se get_vaga_disponivel == –1 → GerenciaFila + erro “SEM_VAGAS”.  
        4) Caso contrário → ocupar_vaga_por_login() e confirmar.

    Hipóteses:
        - ocupar_vaga_por_login() devolve tupla(sucesso,id); usamos apenas efeito.
    """
def AlocarVaga():
    if USUARIO_ATUAL is None:
        TratarErros("NAO_AUTENTICADO")
        return

    est = est_mod.selecionar_estacionamento(ESTACIONAMENTOS)
    if not est:
        print("Nenhum estacionamento selecionado.")
        return

    vaga = est_mod.get_vaga_disponivel(est)
    if vaga is None:
        GerenciaFila(USUARIO_ATUAL)
        TratarErros("SEM_VAGAS")
    else:
        est_mod.ocupar_vaga_por_login(est, usuario_mod.getLogin(USUARIO_ATUAL))
        print(f"✅ Vaga {vaga['id']} ocupada. Boa estadia!")

"""
    Nome: LiberarVaga()

    Objetivo:
        Liberar a vaga ocupada por USUARIO_ATUAL (qualquer estacionamento).

    Acoplamento:
        - Estacionamento.liberar_vaga_de().
        - AtualizarEstado() para realocar fila.

    Condições de Acoplamento:
        AE: USUARIO_ATUAL autentica-do.
        AS: Vaga liberada ou erro VAGA_NAO_ENCONTRADA.

    Descrição:
        Itera todos os estacionamentos:  
        • se liberar_vaga_de() devolver id → imprime sucesso e chama
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
        vaga_id = est_mod.liberar_vaga_de(est, USUARIO_ATUAL)
        if vaga_id is not None:
            print(f"✅ Vaga {vaga_id} liberada no estacionamento '{est_mod.getNome(est)}'.")
            AtualizarEstado(est)
            return

    TratarErros("VAGA_NAO_ENCONTRADA")

"""
    Nome: GerenciaFila(usuario)

    Objetivo:
        Garantir que `usuario` esteja na fila exatamente uma vez, ordenada
        por prioridade (.tipo).

    Acoplamento:
        - fila_mod.consultarPosicaoNaFila, adicionarNaFila.

    Condições de Acoplamento:
        AE: fila do módulo fila_mod inicializada.
        AS: fila contém usuário e está ordenada.

    Descrição:
        Se consultarPosicaoNaFila == –1 → adicionarNaFila().

    Hipóteses:
        - Prioridade: tipo 1 < 2.
    """
def GerenciaFila(usuario):
    if fila_mod.consultarPosicaoNaFila(usuario_mod.getLogin(usuario)) == -1:
        fila_mod.adicionarNaFila(usuario)

"""
    Nome: AtualizarEstado(est)

    Objetivo:
        Após liberação de vaga, chamar o primeiro da fila (se houver).

    Acoplamento:
        - est: Estacionamento onde surgiu vaga.
        - est.getVagaDisponivel() / ocuparVagaPorLogin().
        - fila_mod.retornaPrimeiro / removerDaFila.

    Condições de Acoplamento:
        AE: est válido; fila do módulo fila_mod inicializada.
        AS: Se vaga livre e fila não vazia → ocupação + remoção da fila.

    Descrição:
        1) Verificar vaga livre.  
        2) Se existir, pegar primeiro da fila.  
        3) Tentar ocupar; se sucesso → removerDaFila + mensagem.

    Hipóteses:
        - ocuparVagaPorLogin() retorna (sucesso, id).
    """
def AtualizarEstado(est):
    vaga = est_mod.get_vaga_disponivel(est)
    if vaga is None:
        return

    prox = fila_mod.retornaPrimeiro()
    if prox:
        ok, id_vaga = est_mod.ocupar_vaga_por_login(est, usuario_mod.getLogin(prox))
        if ok:
            fila_mod.removerDaFila(usuario_mod.getLogin(prox))
            print(f"🔔 Usuário {usuario_mod.getLogin(prox)} foi chamado para ocupar a vaga {id_vaga}.")

"""
    Nome: ExibirResumo()

    Objetivo:
        Apresentar visão geral do sistema: vagas por estacionamento, tamanho da
        fila e usuário autenticado.

    Acoplamento:
        - est_mod.listar_estacionamentos().
        - fila_mod.tamanhoFila() e USUARIO_ATUAL.

    Descrição:
        1) Delegar listagem de vagas a est_mod.  
        2) Exibir tamanho da fila.  
        3) Mostrar login do usuário autenticado (ou “Nenhum”).

    Restrições:
        - Apenas saída para console; não altera estado.
    """
def ExibirResumo():
    print("\n=======  RESUMO DO SISTEMA  =======")
    est_mod.listar_estacionamentos(ESTACIONAMENTOS)

    print(f"Usuários na fila: {fila_mod.tamanhoFila()}")
    if USUARIO_ATUAL:
        print(f"Usuário autenticado: {usuario_mod.getLogin(USUARIO_ATUAL)}")
    else:
        print("Nenhum usuário autenticado.")

"""
    Nome: EncerrarSistema()

    Objetivo:
        Persistir usuários, convidados e estado dos estacionamentos em CSV,
        esvaziar a fila e então encerrar o programa.

    Acoplamento:
        - usuario_mod.salvarUsuarios().
        - Estacionamento.salvarEstadoEmCSV() em loop de ESTACIONAMENTOS.
        - fila_mod.esvaziarFila().
        - sys.exit(0).

    Descrição:
        1) Salvar users.csv e guests.csv via usuario_mod.  
        2) Abrir estacionamentos.csv e gravar o snapshot de cada estacionamento.
        3) Esvaziar a fila.
        4) Imprimir confirmação e sair.

    Restrições:
        - Chama sys.exit(), portanto não retorna.
    """
def EncerrarSistema():
    usuario_mod.salvarUsuarios("users.csv", "guests.csv")
    with open("estacionamentos.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for est in ESTACIONAMENTOS:
            est_mod.salvar_estado_em_csv(est, writer)
    
    # Esvaziar a fila antes de encerrar
    fila_mod.esvaziarFila()
    
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
