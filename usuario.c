#include "usuario.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static bool validaLogin(const char* login);
static bool loginExiste(const char* login, Usuario* usuarios, int totalUsuarios);
static bool cpfConvidadoValido(const char* cpf, Usuario* convidados, int totalConvidados);
static Usuario* criaListaUsuarios();

/***************************************************************************************************************
Nome: criaInterno(mtr, senha)

Objetivo:
   - Registrar um novo usuário interno com matrícula e senha.

Acoplamento:
   - mtr   (const char*): string contendo 8 dígitos numéricos da matrícula.
   - senha (const char*): string não vazia representando a senha.
   - retorno (Usuario*): ponteiro para estrutura alocada com dados do usuário,
     ou NULL em caso de erro.

Condições de Acoplamento:
   AE: mtr != NULL && strlen(mtr) == 8 && apenas dígitos em mtr.
   AE: senha != NULL && senha não vazia.
   AS: retorna Usuario* válido alocado em heap com campos login, senha e tipo = INTERNO.
   AS (erro): retorna NULL e imprime mensagem de erro no stderr.

Descrição:
   1) Chama validaLogin(mtr) para checar formato de matrícula.
   2) Chama loginExiste(mtr) para garantir unicidade.
   3) Abre o arquivo "users.csv" em modo "a" para acrescentar registro.
   4) Escreve linha "mtr,senha,INTERNO" e fecha arquivo.
   5) Aloca Usuario em heap, copia strings e define tipo.
   6) Retorna ponteiro para o novo usuário.

Hipóteses:
   - O arquivo users.csv pode ser criado/aberto em modo de append.
   - Permissões de escrita no diretório estão garantidas.

Restrições:
   - Matrícula fixa em 8 dígitos numéricas; sem hífens ou pontos.

**************************************************************************************************************/

Usuario* criaInterno(const char* mtr, const char* senha) {
    // Validar formato da matrícula
    // - Deve ter exatamente 8 caracteres
    // - Todos devem ser dígitos numéricos
    if (!validaLogin(mtr)) {
        // Formato inválido -> registrar erro e abortar
        fprintf(stderr, "Erro: login inválido.\n");
        return NULL;
    }

    // Verificar unicidade da matrícula
    // - Percorrer users.csv procurando por login igual
    if (loginExiste(mtr)) {
        // Se já existir, registrar erro e abortar
        fprintf(stderr, "Erro: login já existe.\n");
        return NULL;
    }

    // Abrir arquivo CSV para anexar novo usuário
    // - Modo "a": mantém conteúdo existente e posiciona no fim
    // - Cria o arquivo se não existir
    FILE* f = fopen("users.csv", "a");
    if (!f) {
        // Erro de abertura (ex.: permissão), reportar e abortar
        perror("users.csv");
        return NULL;
    }

    // Escrever novo registro no CSV
    // - Formato: login,senha,tipo\n
    // - INTERNO é o enum correspondente (valor 1)
    fprintf(f, "%s,%s,%d\n", mtr, senha, INTERNO);

    // Fechar o arquivo para garantir gravação em disco
    fclose(f);

    // Alocar memória para a estrutura Usuario
    Usuario* u = malloc(sizeof *u);
    if (!u) {
        // Falha de alocação, abortar sem log adicional
        return NULL;
    }

    // Preencher campo 'login' na struct
    // - Usar strncpy para segurança, garantindo término nulo
    strncpy(u->login, mtr, MAX_LOGIN_LEN - 1);
    u->login[MAX_LOGIN_LEN - 1] = '\0';

    // Preencher campo 'senha' na struct
    strncpy(u->senha, senha, MAX_SENHA_LEN - 1);
    u->senha[MAX_SENHA_LEN - 1] = '\0';

    // Definir tipo de usuário como INTERNO
    u->tipo = INTERNO;

    // Retornar ponteiro para o novo usuário alocado
    return u;
}


/***************************************************************************************************************
Nome: criaConvidado(cpf, senha)

Objetivo:
   - Registrar um novo usuário convidado para uso único.

Acoplamento:
   - cpf (const char*): string de CPF (formato livre) presente em guests.csv.
   - senha (const char*): string não vazia representando a senha temporária.
   - retorno (Usuario*): ponteiro para estrutura alocada com dados do usuário,
     ou NULL em caso de erro.

Condições de Acoplamento:
   AE: cpf != NULL && string não vazia.
   AE: senha != NULL && senha não vazia.
   AE: cpf consta em guests.csv.
   AS: retorna Usuario* válido alocado em heap com campos login=cpf, senha e tipo=CONVIDADO.
   AS (erro): retorna NULL e imprime mensagem de erro no stderr.

Descrição:
   1) Chama cpfConvidadoValido(cpf) para checar autorização do convidado.
   2) Chama loginExiste(cpf) para garantir que ainda não foi registrado hoje.
   3) Abre "users.csv" em modo "a".
   4) Escreve linha "cpf,senha,CONVIDADO" e fecha arquivo.
   5) Aloca Usuario em heap, copia strings e define tipo.
   6) Retorna ponteiro para o novo usuário.

Hipóteses:
   - guests.csv contém lista atualizada de CPFs convidados do dia.
   - Permissões de escrita em users.csv OK.

**************************************************************************************************************/

Usuario* criaConvidado(const char* cpf, const char* senha) {
    // Verificar se o CPF está autorizado na lista de convidados do dia
    // - Abrir guests.csv e buscar linha igual a cpf
    // - Retornar false se não encontrado
    if (!cpfConvidadoValido(cpf)) {
        // CPF não consta em guests.csv → erro de autorização
        fprintf(stderr, "Erro: CPF não autorizado como convidado hoje.\n");
        return NULL;
    }

    // Garantir que esse convidado ainda não foi registrado hoje
    // - Abrir users.csv e procurar por login igual ao cpf
    // - Se encontrado, significa que já criou um usuário convidado para esse CPF hoje
    if (loginExiste(cpf)) {
        // CPF já tem registro de convidado em users.csv → erro de duplicidade
        fprintf(stderr, "Erro: convidado já registrado hoje.\n");
        return NULL;
    }

    // Abrir arquivo users.csv em modo append para adicionar novo registro
    // - fopen com "a": posiciona no fim ou cria arquivo se não existir
    FILE* f = fopen("users.csv", "a");
    if (!f) {
        // Falha na abertura (permissão, disco cheio, etc.) → log de perror e abortar
        perror("users.csv");
        return NULL;
    }

    // Escrever novo registro CSV
    // - Formato: cpf,senha,tipo\n
    // - CONVIDADO é o valor do enum (2)
    fprintf(f, "%s,%s,%d\n", cpf, senha, CONVIDADO);

    // Fechar o arquivo para garantir flush do buffer e liberar recurso
    fclose(f);

    // Alocar memória para a nova estrutura Usuario
    // - sizeof *u garante tamanho correto, mesmo se Usuario mudar
    Usuario* u = malloc(sizeof *u);
    if (!u) {
        // Falha de alocação de heap → abortar sem log adicional
        return NULL;
    }

    // Copiar o CPF para u->login
    // - strncpy limita cópia a MAX_LOGIN_LEN-1
    // - Garante terminação nula em u->login[MAX_LOGIN_LEN-1]
    strncpy(u->login, cpf, MAX_LOGIN_LEN - 1);
    u->login[MAX_LOGIN_LEN - 1] = '\0';

    // Copiar a senha para u->senha
    // - mesma lógica de segurança de buffer
    strncpy(u->senha, senha, MAX_SENHA_LEN - 1);
    u->senha[MAX_SENHA_LEN - 1] = '\0';

    // Definir o tipo de usuário como CONVIDADO
    u->tipo = CONVIDADO;

    // Retornar ponteiro para a estrutura alocada com dados do convidado
    return u;
}


/***************************************************************************************************************
Nome: getTipo(login)

Objetivo:
   - Determinar o tipo de usuário baseado no registro em users.csv.

Acoplamento:
   - login  (const char*): string que identifica usuário (mtr ou cpf).
   - retorno (TipoUsuario): valor INTERNO, CONVIDADO ou EXTERNO (usuário não cadastrado).

Condições de Acoplamento:
   AE: login != NULL && login não vazio.
   AS: retorna INTERNO se encontrar registro com tipo=1.
   AS: retorna CONVIDADO se encontrar registro com tipo=2.
   AS: retorna EXTERNO caso não encontre ou erro de I/O.

Descrição:
   1) Abre "users.csv" em modo leitura.
   2) Para cada linha, tokeniza pelo delimitador vírgula.
   3) Compara tok_login com parâmetro login.
   4) Se igual, pula senha, lê campo tipo, converte para int e retorna.
   5) Se fim de arquivo sem encontrar, retorna EXTERNO.

Hipóteses:
   - users.csv está acessível para leitura.

**************************************************************************************************************/

TipoUsuario getTipo(const char* login) {
    // Abrir o arquivo de usuários em modo leitura
    // - Se falhar (arquivo inexistente ou sem permissão), reporta erro e considera usuário externo
    FILE* f = fopen("users.csv", "r");
    if (!f) {
        // Erro de I/O ao abrir users.csv → log de perror e retorno EXTERNO
        perror("users.csv");
        return EXTERNO;
    }

    // Buffer para leitura de cada linha do CSV (até 255 chars + '\0')
    char linha[256];

    // Loop de leitura: enquanto houver linha em users.csv
    while (fgets(linha, sizeof linha, f)) {
        // Tokenizar a linha usando vírgula como delimitador
        //     Primeiro token = login cadastrado
        char* tok = strtok(linha, ",");
        // Se o token existe e casa com o login buscado
        if (tok && strcmp(tok, login) == 0) {
            // Encontrou o login desejado
            // Chamar strtok(NULL, ",") para descartar o campo senha
            strtok(NULL, ",");
            // Novo strtok(NULL, ",") para capturar o campo tipo
            char* tipoStr = strtok(NULL, ",");
            // Converter string do tipo para inteiro
            int t = atoi(tipoStr);
            // Fechar o arquivo após uso
            fclose(f);
            // Retornar o enum correspondente ao tipo (1, 2 ou 3)
            return (TipoUsuario)t;
        }
        // Caso tok != login, continuar para a próxima linha
    }

    // Fim do arquivo sem encontrar o login
    // - Fechar arquivo e tratar como usuário externo
    fclose(f);
    return EXTERNO;
}


// Verifica se o login (matrícula) tem exatamente 8 dígitos numéricos
static bool validaLogin(const char* login) {
    if (strlen(login) != 8)
        return false;
    for (const char* p = login; *p; p++) {
        if (!isdigit((unsigned char)*p))
            return false;
    }
    return true;
}

// Verifica se já existe um login igual em usuarios
static bool loginExiste(const char* login, Usuario* usuarios, int totalUsuarios) {
    for (int i = 0; i < totalUsuarios; i++) {
        if (strcmp(usuarios[i].login, login) == 0) {
            return false;
        }
    }
    return true;
}

// Verifica se o CPF consta na lista de convidados do dia
static bool cpfConvidadoValido(const char* cpf, Usuario* convidados, int totalConvidados) {
    for (int i = 0; i < totalConvidados; i++) {
        if (strcmp(convidados[i].login, cpf) == 0) {
            return true;
        }
    }
    return false;
}