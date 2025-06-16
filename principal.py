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
    Nome: ExibirMenuPrincipal()

    Objetivo:
       - Controlar o loop de interação de alto nível com o usuário.

    Acoplamento:
       - leitura: input() para selecionar opção.
       - retorno: None — loop somente termina em EncerrarSistema().

    Condições de Acoplamento:
       AE: IniciarSistema() já executado.
       AS: Usuário navega entre opções 1–5, com tratamento de erro para outras.

    Descrição:
       1) Construir dicionário opcoes {str: função}.
       2) Loop infinito: exibir menu textual, ler escolha.
       3) Se escolha válida → chamar função correspondente.
          Caso contrário → TratarErros("OPCAO_INVALIDA").

    Hipóteses:
       - Todas funções chamadas estão importadas e operacionais.

    Restrições:
       - Executa indefinidamente até EncerrarSistema() chamar sys.exit().
    """
def ExibirMenuPrincipal():
    opcoes = {
        "1": AutenticarUsuario,
        #TODO: "2": CriarUsuario,
        "2": AlocarVaga,
        "3": LiberarVaga,
        "4": ExibirResumo,
        "5": EncerrarSistema
    }
    while True:
        print("\n======  MENU PRINCIPAL  ======")
        print("1) Login")

        #TODO: primeiro mostra o Login, depois mostra o restante do menu
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

"""
    Nome: AutenticarUsuario()

    Objetivo:
       - Solicitar credenciais e validar acesso do usuário.

    Acoplamento:
       - módulos: login.autentica(), usuario.usuarios.
       - leitura: input() (login, senha).
       - efeito: define variável global USUARIO_ATUAL.

    Condições de Acoplamento:
       AE: usuario.usuarios contém tuplas válidas.
       AS: Se credenciais corretas → USUARIO_ATUAL recebe login.
       AS: Se inválidas → TratarErros("AUTH_FAIL").

    Descrição:
       1) Ler login e senha via input().
       2) Chamar login.autentica(login, senha, usuario.usuarios).
       3) Se True → armazenar login, exibir mensagem de boas-vindas.
          Senão → chamar TratarErros("AUTH_FAIL").

    Hipóteses:
       - Função autentica retorna booleano conforme especificação.

    Restrições:
       - Nenhum.
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
       - Tentar reservar uma vaga para o usuário autenticado ou inseri-lo na fila.

    Acoplamento:
       - leitura: variável global USUARIO_ATUAL.
       - módulos previstos: est_mod.getVagaDisponivel(), vaga_mod.OcuparVaga(),
         GerenciaFila().
       - retorno: None.

    Condições de Acoplamento:
       AE: Usuário deve estar autenticado.
       AE: ESTACIONAMENTOS configurado; módulos est_mod/vaga_mod implementados.
       AS: Se vaga disponível → ocupada; senão → usuário entra na fila.

    Descrição:
       1) Verificar autenticação; se não, erro.
       2) Permitir escolha do estacionamento via _selecionar_estacionamento().
       3) Chamar est_mod.getVagaDisponivel(est).
          a. Se -1 → GerenciaFila() + mensagem SEM_VAGAS.
          b. Caso contrário → vaga_mod.OcuparVaga() + confirmação.

    Hipóteses:
       - Funções de est_mod e vaga_mod seguem contrato previsto.

    Restrições:
       - Contém TODOs até implementação dos demais módulos.
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
       - Desocupar uma vaga e disparar atualização de estado (fila).

    Acoplamento:
       - leitura: USUARIO_ATUAL, input() para id da vaga.
       - módulos previstos: vaga_mod.LiberarVaga(), AtualizarEstado().

    Condições de Acoplamento:
       AE: Usuário precisa estar autenticado.
       AE: ID informado deve ser numérico e existente.
       AS: Se sucesso → vaga liberada + AtualizarEstado().
       AS: Se falha → mensagem VAGA_NAO_ENCONTRADA.

    Descrição:
       1) Checar autenticação.
       2) Selecionar estacionamento.
       3) Ler ID da vaga e chamar vaga_mod.LiberarVaga().
       4) Resultado 0 → sucesso; else → erro.
       5) Em sucesso → AtualizarEstado(est).

    Hipóteses:
       - vaga_mod.LiberarVaga retorna 0 em sucesso.

    Restrições:
       - Contém TODOs pendentes.
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
    Nome: GerenciaFila(usuario_login)

    Objetivo:
       - Garantir que o usuário esteja na fila e ordenar por prioridade.

    Acoplamento:
       - FILA global e funções de fila_mod.

    Condições de Acoplamento:
       AE: FILA inicializada.
       AS: Se usuário não presente → adicionado; fila reordenada.

    Descrição:
       1) Consultar posição atual via fila_mod.consultarPosicaoNaFila().
       2) Se -1 → adicionarNaFila().
       3) Ordenar fila por prioridade.

    Hipóteses:
       - Prioridade definida na lógica interna de fila_mod.

    Restrições:
       - Nenhum.
    """
def GerenciaFila(usuario):
    if fila_mod.consultarPosicaoNaFila(FILA, usuario) == -1:
        fila_mod.adicionarNaFila(FILA, usuario)
        fila_mod.ordenarFilaPorPrioridade(FILA)

"""
    Nome: AtualizarEstado(est)

    Objetivo:
       - Após liberação de vaga, realocar primeiro usuário da fila.

    Acoplamento:
       - est_mod.getVagaDisponivel(), fila_mod.* e vaga_mod.OcuparVaga().

    Condições de Acoplamento:
       AE: est é objeto Estacionamento válido.
       AS: Se existir vaga e fila não vazia → ocupar vaga e remover usuário.

    Descrição:
       1) Obter vaga livre via est_mod.getVagaDisponivel().
       2) Se -1 → retornar (nenhuma ação).
       3) Obter primeiro usuário via fila_mod.consultarPosicaoNaFila() ou método próprio.
       4) Se existir → vaga_mod.OcuparVaga() e fila_mod.removerDaFila().
       5) Exibir notificação ao usuário atendido.

    Hipóteses:
       - Métodos de fila_mod e vaga_mod implementados.

    Restrições:
       - Contém TODOs pendentes.
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
       - Mostrar panorama do sistema: vagas, fila e usuário logado.

    Acoplamento:
       - ESTACIONAMENTOS, FILA, USUARIO_ATUAL e est_mod.BuscarVagasDisponiveis().

    Condições de Acoplamento:
       AE: Sistema inicializado.
       AS: Dados impressos no console.

    Descrição:
       1) Iterar sobre ESTACIONAMENTOS: obter vagas livres / total.
       2) Exibir tamanho da FILA (FILA.tamanho).
       3) Exibir USUARIO_ATUAL ou ausência.

    Hipóteses:
       - Objeto FILA possui atributo .tamanho.

    Restrições:
       - Contém TODO para cálculo de vagas livres.
    """
def ExibirResumo():
    print("\n=======  RESUMO DO SISTEMA  =======")
    est_mod.ListarEstacionamentos(ESTACIONAMENTOS)

    tamanho_fila = FILA.tamanho if FILA else 0
    print(f"Usuários na fila: {tamanho_fila}")
    if USUARIO_ATUAL:
        print(f"Usuário autenticado: {USUARIO_ATUAL}")
    else:
        print("Nenhum usuário autenticado.")

"""
    Nome: EncerrarSistema()

    Objetivo:
       - Persistir dados em CSV e finalizar a aplicação.

    Acoplamento:
       - _salvar_csv(), usuario.usuarios, usuario.convidados.

    Condições de Acoplamento:
       AE: Listas globais atualizadas.
       AS: Arquivos ‘usuarios.csv’ e ‘convidados.csv’ sobrescritos.
       AS: Processo encerrado via sys.exit(0).

    Descrição:
       1) Filtrar usuarios sem convidados.
       2) Salvar ambos os CSVs usando _salvar_csv().
       3) Exibir mensagem e chamar sys.exit(0).

    Hipóteses:
       - Função _salvar_csv grava corretamente.

    Restrições:
       - Não retorna (termina execução do Python).
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
       - Exibir mensagem de erro amigável ao usuário.

    Acoplamento:
       - ERROS: dict mapeando códigos → mensagens.

    Condições de Acoplamento:
       AE: codigo é chave existente ou não em ERROS.
       AS: Mensagem correspondente impressa no console.

    Descrição:
       1) Fazer lookup em ERROS.get(codigo, 'Erro desconhecido.').
       2) Imprimir mensagem prefixada por símbolo ⚠️.

    Hipóteses:
       - stdout disponível.

    Restrições:
       - Função simples; não altera estado global.
    """
def TratarErros(codigo):
    print(f"⚠️  {ERROS.get(codigo, 'Erro desconhecido.')}")

# --------------------------- execução direta ---------------------------------
if __name__ == "__main__":
    IniciarSistema()
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
