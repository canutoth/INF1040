#include "login.h"
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// helper: campo válido = não-NULL e não-vazio
static int campo_valido(const char *s) {
    return s && *s;
}

/***************************************************************************************************************
Nome: autentica(login, senha)

Objetivo: validar as credenciais do usuário (login e senha) com base na base de dados de usuários.

Acoplamento:
    - logins: valor do tipo char* a ser validado como a matrícula/cpf do usuário.
    - senha: valor do tipo char* a ser validado como a senha do usuário.
    - retornos: 0 = sucesso; 1 = login inexistente; 2 = senha incorreta; 3 = campos inválidos.

Condições de acoplamento:
    AE: campo login preenchido com um valor do tipo char*.
    AE: campo senha preenchido com um valor do tipo char*.
    AS: informa se o login é válido/inválido.
    AS: informa se a senha corresponde à senha do usuário com aquele login.

Descrição:
    1) Verifica se os parâmetros estão preenchidos e válidos.
    2) Consulta a base de dados de usuários.
    3) Verifica se o login informado existe.
    4) Se existir, compara a senha fornecida com a senha cadastrada.
    5) Retorna o código correspondente conforme o resultado da autenticação.

Hipóteses:
    - A base de dados de usuários está ativa e acessível.
    - O sistema onde a função é executada possui permissões para consultar os dados de autenticação.
****************************************************************************************************************/

int autentica(const char *login, const char *senha) {
    // 1. Verifica se ambos os campos foram preenchidos:
    //    - login != NULL e login não vazio
    //    - senha != NULL e senha não vazio
    // Se qualquer um for inválido, aborta com código de campo inválido.
    if (!campo_valido(login) || !campo_valido(senha))
        return AUTH_INVALID_FIELD;

    // 2. Tenta abrir o arquivo users.csv para leitura.
    //    Se falhar (por exemplo, arquivo não existe ou falta permissão),
    //    usamos perror para imprimir o erro de I/O e retornamos
    //    AUTH_NO_USER (tratando como “usuário não encontrado”).
    FILE *f = fopen("users.csv", "r");
    if (!f) {
        perror("users.csv");
        return AUTH_NO_USER;
    }

    // 3. Buffer para armazenar cada linha lida do CSV (até 255 caracteres + '\0').
    char linha[256];

    // 4. Laço de leitura: enquanto houver linha em users.csv...
    while (fgets(linha, sizeof linha, f)) {
        // 4.1. Usa strtok para separar a string pelo delimitador vírgula:
        //      - primeiro token = login cadastrado
        //      - segundo token   = senha cadastrada
        //      - terceiro token  = tipo (que a gente ignora aqui)
        char *tok_login = strtok(linha, ",");
        char *tok_senha = strtok(NULL, ",");

        // 4.2. Se a linha estiver mal-formada (faltar login ou senha), pula ela.
        if (!tok_login || !tok_senha) 
            continue;

        // 5. Compara o login da linha com o login passado como parâmetro.
        if (strcmp(tok_login, login) == 0) {
            // 5.1. Login encontrado: agora compara as senhas.
            //      Como usamos strtok duas vezes, o ponteiro tok_senha
            //      aponta exatamente ao campo “senha” na linha.
            if (strcmp(tok_senha, senha) == 0) {
                // 5.1.1. Senha coincide: sucesso de autenticação.
                fclose(f);
                return AUTH_SUCCESS;
            } else {
                // 5.1.2. Senha não coincide: usuário existe, mas senha incorreta.
                fclose(f);
                return AUTH_BAD_PASSWORD;
            }
        }
        // 5.3. Se tok_login != login, continua lendo as próximas linhas.
    }

    // 6. Se terminou o arquivo sem encontrar o login: fecha arquivo
    //    e retorna “usuário não encontrado”.
    fclose(f);
    return AUTH_NO_USER;
}