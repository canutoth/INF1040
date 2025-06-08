#include "usuario.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static bool validaLogin(const char* login);
static bool loginExiste(const char* login);
static bool cpfConvidadoValido(const char* cpf);

Usuario* criaInterno(const char* mtr, const char* senha) {
    if (!validaLogin(mtr)) {
        fprintf(stderr, "Erro: login inválido.\n");
        return NULL;
    }
    if (loginExiste(mtr)) {
        fprintf(stderr, "Erro: login já existe.\n");
        return NULL;
    }
    FILE* f = fopen("users.csv", "a");
    if (!f) {
        perror("users.csv");
        return NULL;
    }
    fprintf(f, "%s,%s,%d\n", mtr, senha, INTERNO);
    fclose(f);

    Usuario* u = malloc(sizeof *u);
    if (!u) return NULL;
    strncpy(u->login, mtr, MAX_LOGIN_LEN - 1);
    u->login[MAX_LOGIN_LEN - 1] = '\0';
    strncpy(u->senha, senha, MAX_SENHA_LEN - 1);
    u->senha[MAX_SENHA_LEN - 1] = '\0';
    u->tipo = INTERNO;
    return u;
}

Usuario* criaConvidado(const char* cpf, const char* senha) {
    if (!cpfConvidadoValido(cpf)) {
        fprintf(stderr, "Erro: CPF não autorizado como convidado hoje.\n");
        return NULL;
    }
    if (loginExiste(cpf)) {
        fprintf(stderr, "Erro: convidado já registrado hoje.\n");
        return NULL;
    }
    FILE* f = fopen("users.csv", "a");
    if (!f) {
        perror("users.csv");
        return NULL;
    }
    fprintf(f, "%s,%s,%d\n", cpf, senha, CONVIDADO);
    fclose(f);

    Usuario* u = malloc(sizeof *u);
    if (!u) return NULL;
    strncpy(u->login, cpf, MAX_LOGIN_LEN - 1);
    u->login[MAX_LOGIN_LEN - 1] = '\0';
    strncpy(u->senha, senha, MAX_SENHA_LEN - 1);
    u->senha[MAX_SENHA_LEN - 1] = '\0';
    u->tipo = CONVIDADO;
    return u;
}

TipoUsuario getTipo(const char* login) {
    FILE* f = fopen("users.csv", "r");
    if (!f) {
        perror("users.csv");
        return EXTERNO;
    }
    char linha[256];
    while (fgets(linha, sizeof linha, f)) {
        char* tok = strtok(linha, ",");
        if (tok && strcmp(tok, login) == 0) {
            strtok(NULL, ",");               // pula a senha
            char* tipoStr = strtok(NULL, ",");
            int t = atoi(tipoStr);
            fclose(f);
            return (TipoUsuario)t;
        }
    }
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

// Verifica se já existe um login igual em users.csv
static bool loginExiste(const char* login) {
    FILE* f = fopen("users.csv", "r");
    if (!f) return false;
    char linha[256];
    while (fgets(linha, sizeof linha, f)) {
        char* tok = strtok(linha, ",");
        if (tok && strcmp(tok, login) == 0) {
            fclose(f);
            return true;
        }
    }
    fclose(f);
    return false;
}

// Verifica se o CPF consta na lista de convidados do dia (guests.csv)
static bool cpfConvidadoValido(const char* cpf) {
    FILE* f = fopen("guests.csv", "r");
    if (!f) return false;
    char linha[64];
    while (fgets(linha, sizeof linha, f)) {
        linha[strcspn(linha, "\r\n")] = '\0';
        if (strcmp(linha, cpf) == 0) {
            fclose(f);
            return true;
        }
    }
    fclose(f);
    return false;
}