# principal.py
# -----------------------------------------------------------------------------
# Módulo principal do sistema de gerenciamento de estacionamento
# -----------------------------------------------------------------------------
import csv
import sys
import usuario
import login
import fila        as fila_mod
# import estacionamento as est_mod
# import vaga        as vaga_mod

# ---------------------------- variáveis globais ------------------------------
FILA                = None          # ponteiro para a fila principal
ESTACIONAMENTOS     = []            # lista de objetos/estruturas de estacionamento
USUARIO_ATUAL       = None          # login do usuário com sessão ativa

# Mapa simples de erros para mensagens
ERROS = {
    "OPCAO_INVALIDA" : "Opção inválida!",
    "NAO_AUTENTICADO": "É preciso estar autenticado para realizar esta operação.",
    "AUTH_FAIL"      : "Login ou senha incorretos.",
    "SEM_VAGAS"      : "Não há vagas disponíveis neste momento – você foi colocado(a) na fila.",
    "VAGA_NAO_ENCONTRADA": "Vaga inexistente.",
}

# ---------------------------- utilidades internas ----------------------------
def _carregar_csv(caminho):
    dados = []
    try:
        with open(caminho, newline='', encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if row:                        # login ; senha ; tipo
                    dados.append((row[0], row[1], int(row[2])))
    except FileNotFoundError:
        pass                                   # primeiro uso: arquivos ainda não existem
    return dados

def _salvar_csv(caminho, dados):
    with open(caminho, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(dados)

def _selecionar_estacionamento():
    """Pede ao usuário qual estacionamento deseja usar e devolve o objeto escolhido."""
    if not ESTACIONAMENTOS:
        return None
    print("\nEstacionamentos disponíveis:")
    for idx, est in enumerate(ESTACIONAMENTOS, 1):
        print(f"{idx}. {est.nome} – vagas livres: {est.vagas_livres}")
    try:
        op = int(input("Escolha (número) › "))
        return ESTACIONAMENTOS[op-1]
    except (ValueError, IndexError):
        TratarErros("OPCAO_INVALIDA")
        return None

# ------------------------------ rotinas chave -------------------------------
def IniciarSistema():
    """Carrega CSVs, inicializa fila, estacionamentos e variáveis globais."""
    global FILA, ESTACIONAMENTOS

    # 1. Carregar usuários e convidados
    usuario.usuarios   = _carregar_csv("usuarios.csv")
    usuario.convidados = _carregar_csv("convidados.csv")
    usuario.usuarios.extend(usuario.convidados)      # acopla convidados à lista principal

    # 2. Fila
    FILA = fila_mod.inicializarFila()

    # 3. Estacionamentos 
    """
    TODO: Ler estado dos estacionamentos
    try:
        ESTACIONAMENTOS = est_mod.criar_estacionamentos_padrao()
    except AttributeError:
        ESTACIONAMENTOS = [
            est_mod.Estacionamento("Bloco A", 10),
            est_mod.Estacionamento("Bloco B", 10),
        ] 
    """
    print("✅ Sistema iniciado com sucesso.")

def ExibirMenuPrincipal():
    """Loop principal de interação."""
    opcoes = {
        "1": AutenticarUsuario,
        "2": AlocarVaga,
        "3": LiberarVaga,
        "4": ExibirResumo,
        "5": EncerrarSistema
    }
    while True:
        print("\n======  MENU PRINCIPAL  ======")
        print("1) Login")
        print("2) Alocar vaga")
        print("3) Liberar vaga")
        print("4) Exibir resumo")
        print("5) Sair")
        escolha = input("Escolha › ").strip()

        acao = opcoes.get(escolha)
        if acao:
            acao()
        else:
            TratarErros("OPCAO_INVALIDA")

def AutenticarUsuario():
    """Solicita login/senha e efetua autenticação."""
    global USUARIO_ATUAL
    login_inp = input("Login › ").strip()
    senha_inp = input("Senha › ").strip()

    if login.autentica(login_inp, senha_inp, usuario.usuarios):
        USUARIO_ATUAL = login_inp
        print(f"✅ Bem-vindo(a), {USUARIO_ATUAL}!")
    else:
        TratarErros("AUTH_FAIL")

def AlocarVaga():
    """Tenta ocupar uma vaga ou coloca o usuário na fila."""
    if USUARIO_ATUAL is None:
        TratarErros("NAO_AUTENTICADO")
        return

    est = _selecionar_estacionamento()
    if not est:
        return

    # TODO: vaga_disp = est_mod.getVagaDisponivel(est)
    if vaga_disp == -1:
        GerenciaFila(USUARIO_ATUAL)
        TratarErros("SEM_VAGAS")
    else:
        # TODO: vaga_mod.OcuparVaga(vaga_disp, est)
        print(f"✅ Vaga {vaga_disp} ocupada. Boa estadia!")

def LiberarVaga():
    """Libera vaga ocupada e chama AtualizarEstado."""
    if USUARIO_ATUAL is None:
        TratarErros("NAO_AUTENTICADO")
        return

    est = _selecionar_estacionamento()
    if not est:
        return

    try:
        vaga_id = int(input("Informe o ID da vaga a liberar › "))
    except ValueError:
        TratarErros("OPCAO_INVALIDA")
        return

    # TODO: resultado = vaga_mod.LiberarVaga(vaga_id, est)
    if resultado == 0:
        print("✅ Vaga liberada.")
        AtualizarEstado(est)
    else:
        TratarErros("VAGA_NAO_ENCONTRADA")

def GerenciaFila(usuario_login):
    """Insere usuário na fila se ainda não estiver e reordena por prioridade."""
    if fila_mod.consultarPosicaoNaFila(FILA, usuario_login) == -1:
        fila_mod.adicionarNaFila(FILA, usuario_login)
        fila_mod.ordenarFilaPorPrioridade(FILA)

def AtualizarEstado(est):
    """Verifica vagas recém-liberadas e realoca primeiro da fila."""
    # TODO: vaga_disp = est_mod.getVagaDisponivel(est)
    if vaga_disp == -1:
        return

    # há vaga livre – verificar fila
    prox = fila_mod.consultarPosicaoNaFila(FILA, None)  
    if prox != -1:
        # TODO: vaga_mod.OcuparVaga(vaga_disp, est)
        fila_mod.removerDaFila(FILA, prox)
        print(f"🔔 Usuário {prox} foi chamado para ocupar a vaga {vaga_disp}.")

def ExibirResumo():
    """Mostra visão geral do sistema."""
    print("\n=======  RESUMO DO SISTEMA  =======")
    for est in ESTACIONAMENTOS:
        # TODO: livres = est_mod.BuscarVagasDisponiveis(est)
        print(f"{est.nome}: {livres}/{est.total_vagas} vagas livres")

    tamanho_fila = FILA.tamanho if FILA else 0
    print(f"Usuários na fila: {tamanho_fila}")
    if USUARIO_ATUAL:
        print(f"Usuário autenticado: {USUARIO_ATUAL}")
    else:
        print("Nenhum usuário autenticado.")

def EncerrarSistema():
    """Grava CSVs atualizados e encerra o programa."""
    # Desacopla convidados antes de salvar
    lista_somente_usuarios = [u for u in usuario.usuarios if u not in usuario.convidados]
    _salvar_csv("usuarios.csv", lista_somente_usuarios)
    _salvar_csv("convidados.csv", usuario.convidados)
    print("✔️  Dados salvos. Até logo!")
    sys.exit(0)

def TratarErros(codigo):
    """Exibe mensagem amigável de erro."""
    print(f"⚠️  {ERROS.get(codigo, 'Erro desconhecido.')}")

# --------------------------- execução direta ---------------------------------
if __name__ == "__main__":
    IniciarSistema()
    ExibirMenuPrincipal()
