#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "login.h"
#include "usuario.h"
// #include "fila.h"
// #include "estacionamento.h"
// #include "vaga.h"

static char usuario_sessao[MAX_LOGIN_LEN] = "";

/***************************************************************************************************************
Nome: IniciarSistema()

Objetivo:
    - Inicializar os componentes essenciais do sistema antes do início da interação com o usuário.

Acoplamento:
    - Nenhum parâmetro de entrada ou retorno.
    - Interações diretas com módulos como fila, estacionamento, etc. (a serem definidos).

Condições de acoplamento:
    AE: deve ser chamada no início da execução.
    AS: estruturas necessárias para execução normal estão preparadas.

Descrição:
    1) Inicializa estruturas como fila e estacionamentos.
    2) Prepara recursos para alocação de vagas e login de usuários.

Hipóteses:
    - Funções auxiliares de inicialização estão implementadas corretamente.
****************************************************************************************************************/
void IniciarSistema() {
    printf("Inicializando o sistema...\n");
    // TODO: chamar função inicializarFila()
    // TODO: chamar função para instanciar estacionamentos e vagas
    printf("Sistema iniciado com sucesso.\n");
}

/***************************************************************************************************************
Nome: ExibirMenuPrincipal()

Objetivo:
    - Apresentar as opções de uso do sistema ao usuário e executar a ação escolhida.

Acoplamento:
    - Leitura via stdin.
    - Chamada de funções locais como AutenticarUsuario, AlocarVaga, etc.

Condições de acoplamento:
    AE: sistema inicializado corretamente.
    AS: uma ação adequada é executada conforme escolha do usuário.

Descrição:
    1) Exibe menu de opções.
    2) Lê entrada do usuário via scanf.
    3) Encaminha para função correspondente.
****************************************************************************************************************/
void ExibirMenuPrincipal() {
    int opcao;
    printf("\n--- Menu Principal ---\n");
    printf("1. Login\n2. Consultar Vagas\n3. Alocar Vaga\n4. Liberar Vaga\n5. Exibir Resumo\n6. Sair\n");
    printf("Escolha uma opção: ");
    scanf("%d", &opcao);

    switch (opcao) {
        case 1: AutenticarUsuario(); break;
        case 2: ExibirResumo(); break;
        case 3: AlocarVaga(); break;
        case 4: LiberarVaga(); break;
        case 5: ExibirResumo(); break;
        case 6: EncerrarSistema(); exit(0);
        default: printf("Opção inválida.\n");
    }
}

/***************************************************************************************************************
Nome: AutenticarUsuario()

Objetivo:
    - Solicitar login e senha do usuário via entrada padrão.
    - Validar as credenciais informadas utilizando o módulo de autenticação.
    - Armazenar o identificador do usuário na sessão ativa em caso de sucesso.
    - Exibir mensagem de erro apropriada em caso de falha.

Acoplamento:
    - Entrada: login e senha (strings fornecidas pelo usuário via stdin).
    - Saída: impressão em stdout (mensagens de sucesso ou erro).
    - Dependência direta do módulo `login` via chamada a autentica().
    - Dependência indireta de arquivos CSV (`users.csv`) manipulados internamente pelo módulo login.
    - Atualização da variável global `usuario_sessao`.

Condições de acoplamento:
    AE: usuário fornecerá strings válidas via scanf para login e senha.
    AE: função autentica(const char*, const char*) já implementada e funcional.
    AS: se sucesso, login copiado para `usuario_sessao`.
    AS: se falha, exibe mensagem adequada conforme código de erro.

Descrição:
    1) Solicita ao usuário a inserção de login e senha via terminal.
    2) Invoca a função `autentica(login, senha)` para verificar as credenciais.
    3) Se retorno for igual a AUTH_SUCCESS (0):
        - Armazena o login em `usuario_sessao`.
        - Exibe mensagem de autenticação bem-sucedida.
    4) Se retorno for diferente de AUTH_SUCCESS:
        - Chama a função TratarErros() passando o código de retorno.
****************************************************************************************************************/
void AutenticarUsuario() {
    char login[64], senha[64];
    printf("Login: "); scanf("%63s", login);
    printf("Senha: "); scanf("%63s", senha);
    int resultado = autentica(login, senha);
    if (resultado == AUTH_SUCCESS) {
        strncpy(usuario_sessao, login, MAX_LOGIN_LEN - 1);
        usuario_sessao[MAX_LOGIN_LEN - 1] = '\0';
        printf("Autenticação realizada com sucesso!\n");
    } else {
        TratarErros(resultado);
    }
}

/***************************************************************************************************************
Nome: AlocarVaga()

Objetivo:
    - Direcionar o usuário para alocação de vaga se houver disponibilidade ou encaminhar para fila.

Acoplamento:
    - Interação com o módulo Estacionamento e Fila.
    - Utiliza o usuário autenticado armazenado em `usuario_sessao`.

Condições de acoplamento:
    AE: usuário autenticado.
    AS: vaga alocada ou usuário adicionado à fila.

Descrição:
    1) Chama getVagaDisponivel().
    2) Se houver vaga, chama OcuparVaga().
    3) Se não houver, chama GerenciaFila().
****************************************************************************************************************/
void AlocarVaga() {
    if (strlen(usuario_sessao) == 0) {
        printf("Erro: usuário não autenticado.\n");
        return;
    }
    // TODO: chamar função getVagaDisponivel()
    // TODO: se -1, chamar GerenciaFila(usuario_sessao)
    // TODO: senão, chamar OcuparVaga()
}

/***************************************************************************************************************
Nome: LiberarVaga()

Objetivo:
    - Liberar uma vaga ocupada e atualizar o estado do sistema.

Acoplamento:
    - Módulo Vaga e atualização de fila.

Condições de acoplamento:
    AE: vaga ocupada por usuário.
    AS: vaga liberada; se houver fila, um novo usuário pode ser alocado.

Descrição:
    1) Chama LiberarVaga().
    2) Executa AtualizarEstado() para processar fila.
****************************************************************************************************************/
void LiberarVaga() {
    if (strlen(usuario_sessao) == 0) {
        printf("Erro: usuário não autenticado.\n");
        return;
    }
    // TODO: chamar função LiberarVaga()
    // TODO: chamar função AtualizarEstado()
}

/***************************************************************************************************************
Nome: GerenciaFila(usuario)

Objetivo:
    - Inserir usuário na fila de espera por vaga, se não estiver presente.

Acoplamento:
    - Módulo Fila: consultarPosicaoNaFila(), adicionarNaFila(), ordenarFilaPorPrioridade().

Condições de acoplamento:
    AE: login válido.
    AS: usuário adicionado e fila reordenada.

Descrição:
    1) Verifica se já está na fila.
    2) Se não, adiciona e ordena.
****************************************************************************************************************/
void GerenciaFila(const char* usuario) {
    // TODO: chamar consultarPosicaoNaFila()
    // TODO: se não estiver na fila, chamar adicionarNaFila() e ordenarFilaPorPrioridade()
}

/***************************************************************************************************************
Nome: AtualizarEstado()

Objetivo:
    - Verificar se há vagas disponíveis e alocar próximo da fila se for o caso.

Acoplamento:
    - Módulo Estacionamento e Fila.

Condições de acoplamento:
    AE: fila inicializada.
    AS: aloca vaga se houver disponível; remove da fila o alocado.

Descrição:
    1) Verifica vagas livres.
    2) Se houver, identifica próximo na fila.
    3) Realiza alocação e remove da fila.
****************************************************************************************************************/
void AtualizarEstado() {
    // TODO: chamar getVagaDisponivel()
    // TODO: se != -1, consultarPosicaoNaFila(), ocuparVaga(), removerDaFila()
}

/***************************************************************************************************************
Nome: ExibirResumo()

Objetivo:
    - Apresentar um panorama geral do estado atual do sistema para o usuário.

Acoplamento:
    - Variável `usuario_sessao`, fila, e status de estacionamentos.

Condições de acoplamento:
    AE: sistema inicializado.
    AS: informações apresentadas corretamente na tela.

Descrição:
    1) Mostra login da sessão ativa.
    2) Exibe quantidade de vagas totais e livres.
    3) Exibe tamanho da fila.
****************************************************************************************************************/
void ExibirResumo() {
    printf("\n--- Resumo do Sistema ---\n");
    printf("Usuário autenticado: %s\n", strlen(usuario_sessao) ? usuario_sessao : "(nenhum)");
    // TODO: chamar ListarEstacionamentos()
    // TODO: exibir número de usuários na fila
}

/***************************************************************************************************************
Nome: EncerrarSistema()

Objetivo:
    - Finalizar execução, liberando recursos e encerrando arquivos.

Acoplamento:
    - Recursos de memória e arquivos (fila, listas, logs, etc).

Condições de acoplamento:
    AE: sistema em execução.
    AS: termina o programa sem vazamentos ou recursos abertos.

Descrição:
    1) Libera estruturas alocadas.
    2) Fecha arquivos, se abertos.
    3) Finaliza aplicação.
****************************************************************************************************************/
void EncerrarSistema() {
    printf("Encerrando sistema...\n");
    // TODO: chamar liberarFila()
    // TODO: chamar salvarEstado()
}

/***************************************************************************************************************
Nome: TratarErros(codigo)

Objetivo:
    - Exibir mensagens claras de erro com base no código de retorno das funções.

Acoplamento:
    - Códigos de erro definidos em login.h (ex: AUTH_NO_USER, AUTH_BAD_PASSWORD, etc).

Condições de acoplamento:
    AE: chamada após falha em operação com código retornado.
    AS: mensagem de erro exibida ao usuário.

Descrição:
    1) Avalia valor inteiro de erro.
    2) Usa switch/case para mapear mensagens informativas.
****************************************************************************************************************/
void TratarErros(int codigo) {
    switch (codigo) {
        case AUTH_NO_USER:
            printf("Erro: usuário não encontrado.\n");
            break;
        case AUTH_BAD_PASSWORD:
            printf("Erro: senha incorreta.\n");
            break;
        case AUTH_INVALID_FIELD:
            printf("Erro: campos de login e/ou senha inválidos.\n");
            break;
        default:
            printf("Erro desconhecido.\n");
    }
}
