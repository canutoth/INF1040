#include "login.h"
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// helper: campo válido = não-NULL e não-vazio
static int campo_valido(const char *s) {
    return s && *s;
}

int autentica(const char *login, const char *senha) {
    if (!campo_valido(login) || !campo_valido(senha))
        return AUTH_INVALID_FIELD;

    FILE *f = fopen("users.csv", "r");
    if (!f) {
        perror("users.csv");
        return AUTH_NO_USER;
    }

    char linha[256];
    while (fgets(linha, sizeof linha, f)) {
        // Espera formato: login,senha,tipo\n
        char *tok_login = strtok(linha, ",");
        char *tok_senha = strtok(NULL, ",");
        if (!tok_login || !tok_senha) 
            continue;

        if (strcmp(tok_login, login) == 0) {
            // achou o usuário: compara senha
            // strtok() consumiu só até a senha; podemos ignorar o tipo
            if (strcmp(tok_senha, senha) == 0) {
                fclose(f);
                return AUTH_SUCCESS;
            } else {
                fclose(f);
                return AUTH_BAD_PASSWORD;
            }
        }
    }

    fclose(f);
    return AUTH_NO_USER;
}
