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

int autentica(const char *login, const char *senha, Usuario* usuarios, int totalUsuarios) {
    if (!campo_valido(login) || !campo_valido(senha))
        return AUTH_INVALID_FIELD;

    for (int i = 0; i < totalUsuarios; i++) {
        if (strcmp(usuarios[i].login, login) == 0) {
            return strcmp(usuarios[i].senha, senha) == 0
                   ? AUTH_SUCCESS : AUTH_BAD_PASSWORD;
        }
    }
    return AUTH_NO_USER;
}