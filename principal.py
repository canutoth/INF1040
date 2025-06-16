# principal.py
# -----------------------------------------------------------------------------
# Módulo principal do sistema de gerenciamento de estacionamento
# -----------------------------------------------------------------------------
import csv
import sys
import usuario
import login
import fila        as fila_mod
import estacionamento as est_mod
import vagas        as vaga_mod

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
"""
    Nome: _carregar_csv(caminho)

    Objetivo:
       - Ler um arquivo .csv delimitado por ‘;’ e convertê-lo em lista de tuplas.

    Acoplamento:
       - caminho: str — path para o arquivo .csv.
       - retorno: list[tuple[str, str, int]] — cada tupla → (login, senha, tipo).

    Condições de Acoplamento:
       AE: caminho deve apontar para um arquivo .csv válido ou inexistente.
       AS: Caso o arquivo exista, retorna estrutura list[...] com os registros lidos.
       AS: Se o arquivo não existir, retorna lista vazia (primeira execução).

    Descrição:
       1) Tentar abrir o arquivo no modo leitura, encoding UTF-8.
       2) Iterar sobre csv.reader(), convertendo cada linha não vazia
          em (login, senha, int(tipo)).
       3) Em FileNotFoundError, capturar exceção e retornar [].

    Hipóteses:
       - Arquivo, se existir, está formatado como “login;senha;tipo”.

    Restrições:
       - Não cria nem modifica arquivos; somente leitura.
    """
def _carregar_csv(caminho, tipo_padrao=None):
    dados = []
    try:
        with open(caminho, newline='', encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if not row:
                    continue  # ignora linhas completamente vazias
                login = row[0].strip() if len(row) > 0 else ""
                senha = row[1].strip() if len(row) > 1 else ""
                try:
                    tipo = int(row[2]) if len(row) > 2 else tipo_padrao
                except ValueError:
                    tipo = tipo_padrao  # ignora erro de conversão e usa padrão

                if login and senha and tipo is not None:
                    dados.append((login, senha, tipo))
    except FileNotFoundError:
        pass
    return dados

"""
    Nome: _salvar_csv(caminho, dados)

    Objetivo:
       - Persistir em disco a lista de tuplas recebida, no formato CSV ‘;’.

    Acoplamento:
       - caminho: str — destino do arquivo .csv.
       - dados: list[tuple] — estrutura já validada a ser gravada.
       - retorno: None.

    Condições de Acoplamento:
       AE: dados deve ser iterável contendo sub-iteráveis (tuplas ou listas).
       AS: Arquivo é sobrescrito/ criado com conteúdo de dados.

    Descrição:
       1) Abrir (ou criar) o arquivo no modo escrita, encoding UTF-8.
       2) Utilizar csv.writer(delimiter=';') para gravar cada tupla.

    Hipóteses:
       - Permissões de escrita no diretório estão concedidas.

    Restrições:
       - Sobrescreve totalmente o arquivo; não há append incremental.
    """
def _salvar_csv(caminho, dados):
    with open(caminho, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(dados)

"""
    Nome: _selecionar_estacionamento()

    Objetivo:
       - Permitir ao usuário escolher qual estacionamento operar.

    Acoplamento:
       - leitura: input() do usuário (número do estacionamento).
       - retorno: objeto Estacionamento selecionado ou None em erro.

    Condições de Acoplamento:
       AE: ESTACIONAMENTOS é lista de objetos com atributos .nome e .vagas_livres.
       AS: Retorna instância escolhida ou None se opção inválida.

    Descrição:
       1) Exibir índice e nome de cada estacionamento com vagas livres.
       2) Ler escolha, converter para int e retornar ESTACIONAMENTOS[idx-1].
       3) Em ValueError ou IndexError → TratarErros("OPCAO_INVALIDA") + None.

    Hipóteses:
       - Lista ESTACIONAMENTOS foi previamente preenchida.

    Restrições:
       - Função interna; não deve ser chamada fora do módulo principal.
    """
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
"""
    Nome: _carregar_csv(caminho, tipo_padrao=None)

    Objetivo:
       - Ler um arquivo .csv delimitado por vírgulas (`,`), convertendo cada linha em tupla (login, senha, tipo).
       - Se a coluna de tipo não estiver presente na linha, utiliza o valor definido em tipo_padrao (se fornecido).

    Parâmetros:
       - caminho (str): Caminho do arquivo .csv a ser lido.
       - tipo_padrao (int | None): Valor a ser usado como tipo caso a linha possua apenas login e senha.

    Retorno:
       - list[tuple[str, str, int]]: Lista de tuplas com as informações (login, senha, tipo).

    Comportamento:
       1) Tenta abrir o arquivo usando codificação UTF-8.
       2) Lê linha por linha com separador `,`.
       3) Para cada linha:
          a) Ignora linhas completamente vazias.
          b) Lê login e senha (obrigatórios).
          c) Lê o tipo, se disponível; caso contrário, utiliza tipo_padrao.
          d) Linhas com campos ausentes ou tipo indefinido são ignoradas.
       4) Em caso de erro de leitura ou ausência do arquivo, retorna lista vazia.

    Hipóteses:
       - O arquivo pode conter registros com 2 ou 3 colunas.
       - O tipo é convertido para `int` caso esteja presente na linha.

    Restrições:
       - Linhas inválidas (com campos ausentes ou mal formatadas) são descartadas silenciosamente.
       - O tipo_padrao deve ser fornecido quando se espera arquivos sem a coluna tipo.
"""
def IniciarSistema():
    """Carrega CSVs, inicializa fila, estacionamentos e variáveis globais."""
    global FILA, ESTACIONAMENTOS

    # 1. Carregar usuários e convidados
    usuario.usuarios   = _carregar_csv("users.csv")
    print("Usuários carregados:", usuario.usuarios)
    usuario.convidados = _carregar_csv("guests.csv", tipo_padrao=2)
    usuario.usuarios.extend(usuario.convidados)
    print("Usuários após adicionar convidados:", usuario.usuarios)

    # 2. Fila
    FILA = fila_mod.inicializarFila()

    # 3. Estacionamentos 
    #TODO: criar um arquivo base dos dados dos estacionamentos, com quantidade de vagas e etc
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
    """Loop principal de interação."""
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
    """Solicita login/senha e efetua autenticação."""
    global USUARIO_ATUAL
    login_inp = input("Login › ").strip()
    senha_inp = input("Senha › ").strip()

    if login.autentica(login_inp, senha_inp, usuario.usuarios):
        USUARIO_ATUAL = login_inp
        print(f"✅ Bem-vindo(a), {USUARIO_ATUAL}!")
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
    """Tenta ocupar uma vaga ou coloca o usuário na fila."""
    if USUARIO_ATUAL is None:
        TratarErros("NAO_AUTENTICADO")
        return

    est = _selecionar_estacionamento()
    if not est:
        print("Nenhum estacionamento selecionado para alocar vaga")
        return

    vaga_disp = est_mod.getVagaDisponivel(est)
    if vaga_disp == -1:
        GerenciaFila(USUARIO_ATUAL)
        TratarErros("SEM_VAGAS")
    else:
        vaga_mod.OcuparVaga(vaga_disp, est)
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
    """Libera vaga ocupada e chama AtualizarEstado."""
    if USUARIO_ATUAL is None:
        TratarErros("NAO_AUTENTICADO")
        return

    est = _selecionar_estacionamento()
    if not est:
        print("Nenhum estacionamento selecionado para liberar vaga")
        return

    try:
        vaga_id = int(input("Informe o ID da vaga a liberar › "))
    except ValueError:
        TratarErros("OPCAO_INVALIDA")
        return

    resultado = vaga_mod.LiberarVaga(vaga_id, est)
    if resultado == 0:
        print("✅ Vaga liberada.")
        AtualizarEstado(est)
    else:
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
def GerenciaFila(usuario_login):
    """Insere usuário na fila se ainda não estiver e reordena por prioridade."""
    if fila_mod.consultarPosicaoNaFila(FILA, usuario_login) == -1:
        fila_mod.adicionarNaFila(FILA, usuario_login)
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
    """Verifica vagas recém-liberadas e realoca primeiro da fila."""
    vaga_disp = est_mod.getVagaDisponivel(est)
    if vaga_disp == -1:
        return

    # há vaga livre – verificar fila
    prox = fila_mod.retornaPrimeiro(FILA)  
    if prox != None:
        #TODO: vaga_mod.OcuparVaga(vaga_disp, est, prox.getLogin)
        #TODO: criar função getLogin no módulo usuário
        fila_mod.removerDaFila(FILA, prox)
        print(f"🔔 Usuário {prox} foi chamado para ocupar a vaga {vaga_disp}.")

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
    """Mostra visão geral do sistema."""
    print("\n=======  RESUMO DO SISTEMA  =======")
    for est in ESTACIONAMENTOS:
        livres = est_mod.BuscarVagasDisponiveis(est)
        print(f"{est.nome}: {livres}/{est.total_vagas} vagas livres")

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
    """Grava CSVs atualizados e encerra o programa."""
    # Desacopla convidados antes de salvar
    lista_somente_usuarios = [u for u in usuario.usuarios if u not in usuario.convidados]
    _salvar_csv("users.csv", lista_somente_usuarios)
    _salvar_csv("guests.csv", usuario.convidados)
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
    """Exibe mensagem amigável de erro."""
    print(f"⚠️  {ERROS.get(codigo, 'Erro desconhecido.')}")

# --------------------------- execução direta ---------------------------------
if __name__ == "__main__":
    IniciarSistema()
    ExibirMenuPrincipal()
