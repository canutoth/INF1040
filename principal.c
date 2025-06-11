#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "login.h"
#include "usuario.h"
// #include "fila.h"

// Sessão ativa: identificador de login do usuário autenticado
static char usuario_sessao[MAX_LOGIN_LEN] = "";

// Prototipações
void IniciarSistema();
void ExibirMenuPrincipal();
void AutenticarUsuario();
void AlocarVaga();
void LiberarVaga();
void GerenciaFila(const char* usuario);
void AtualizarEstado();
void ExibirResumo();
void EncerrarSistema();
void TratarErros(int codigo);

// Função principal
int main(void) {
    IniciarSistema();
    while (1) {
        ExibirMenuPrincipal();
    }
    EncerrarSistema();
    return 0;
}

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

    // Exemplo: inicializar fila
    // inicializarFila(&fila_global);

    // TODO: instanciar estacionamentos e vagas
    // TODO: carregar dados persistentes, se houver

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
 *************************************************************************************************/
void ExibirMenuPrincipal() {
    int opcao;

    printf("\n--- Menu Principal ---\n");
    printf("1. Login\n");
    printf("2. Consultar Vagas\n");
    printf("3. Alocar Vaga\n");
    printf("4. Liberar Vaga\n");
    printf("5. Exibir Resumo\n");
    printf("6. Sair\n");
    printf("Escolha uma opção: ");
    scanf("%d", &opcao);

    switch (opcao) {
        case 1:
            AutenticarUsuario();
            break;
        case 2:
            // TODO: implementar consulta de vagas
            break;
        case 3:
            AlocarVaga();
            break;
        case 4:
            LiberarVaga();
            break;
        case 5:
            ExibirResumo();
            break;
        case 6:
            EncerrarSistema();
            exit(0);
        default:
            printf("Opção inválida.\n");
    }
}

/*************************************************************************************************
 * AutenticarUsuario
 * Solicita login e senha, autentica via módulo Login e armazena usuário na sessão
 *************************************************************************************************/
void AutenticarUsuario() {
    char login[64], senha[64];
    printf("Login: ");
    scanf("%s", login);
    printf("Senha: ");
    scanf("%s", senha);

    int resultado = autentica(login, senha);
    if (resultado == AUTH_SUCCESS) {
        strncpy(usuario_sessao, login, MAX_LOGIN_LEN - 1);
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
    // TODO: usar getVagaDisponivel() e lógica de decisão
    printf("Função de alocação de vaga chamada.\n");
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
    // TODO: lógica de liberação de vaga
    printf("Função de liberação de vaga chamada.\n");
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
    // TODO: verificar se já está na fila e adicionar se necessário
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
    // TODO: verificar disponibilidade e movimentar fila
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
    printf("Usuário autenticado: %s\n", strlen(usuario_sessao) ? usuario_sessao : "(nenhum)\n");
    // TODO: mostrar vagas disponíveis, usuários na fila etc.
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
    // TODO: liberar memória, salvar estado, etc.
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

int carregarUsuariosCSV(const char* nomeArquivo, Usuario* usuarios, int maxUsuarios) {
    FILE* f = fopen(nomeArquivo, "r");
    if (!f) return -1;

    int count = 0;
    char linha[256];
    while (fgets(linha, sizeof linha, f) && count < maxUsuarios) {
        char *login = strtok(linha, ",");
        char *senha = strtok(NULL, ",");
        char *tipo = strtok(NULL, ",\r\n");

        if (login && senha && tipo) {
            strncpy(usuarios[count].login, login, MAX_LOGIN_LEN - 1);
            strncpy(usuarios[count].senha, senha, MAX_SENHA_LEN - 1);
            usuarios[count].tipo = atoi(tipo);
            count++;
        }
    }
    fclose(f);
    return count;
}
