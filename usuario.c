#include <stdlib.h>
#include <stdio.h>
#include "usuario.h"

/* Externs definidos em main.c */
extern cJSON *internalUsers;
extern cJSON *guestList;

Usuario *criaInterno(long long mtr, int senha) {
    if (mtr <= 0 || senha <= 0) {
        fprintf(stderr, "criaInterno: campos inválidos\n");
        return NULL;
    }
    if (!cJSON_IsArray(internalUsers)) {
        fprintf(stderr, "criaInterno: internalUsers inválido\n");
        return NULL;
    }
    /* verifica unicidade */
    cJSON *u;
    cJSON_ArrayForEach(u, internalUsers) {
        cJSON *jl = cJSON_GetObjectItemCaseSensitive(u, "login");
        if (cJSON_IsNumber(jl) && jl->valuedouble == (double)mtr) {
            fprintf(stderr, "criaInterno: matrícula já existe\n");
            return NULL;
        }
    }
    /* adiciona ao JSON interno */
    cJSON *novo = cJSON_CreateObject();
    cJSON_AddNumberToObject(novo, "login", (double)mtr);
    cJSON_AddNumberToObject(novo, "senha", senha);
    cJSON_AddItemToArray(internalUsers, novo);

    /* retorna struct preenchida */
    Usuario *usr = malloc(sizeof(Usuario));
    if (!usr) return NULL;
    usr->login  = mtr;
    usr->senha  = senha;
    usr->tipo   = getTipo(mtr);
    return usr;
}

Usuario *criaConvidado(long long cpf, int senha) {
    if (cpf <= 0 || senha <= 0) {
        fprintf(stderr, "criaConvidado: campos inválidos\n");
        return NULL;
    }
    if (!cJSON_IsArray(guestList)) {
        fprintf(stderr, "criaConvidado: guestList inválido\n");
        return NULL;
    }
    /* procura CPF na lista do dia */
    cJSON *item;
    cJSON_ArrayForEach(item, guestList) {
        if (cJSON_IsNumber(item) && item->valuedouble == (double)cpf) {
            Usuario *usr = malloc(sizeof(Usuario));
            if (!usr) return NULL;
            usr->login = cpf;
            usr->senha = senha;
            usr->tipo  = getTipo(cpf);
            return usr;
        }
    }
    fprintf(stderr, "criaConvidado: CPF não está na lista\n");
    return NULL;
}

int getTipo(long long login) {
    /* interno? */
    if (cJSON_IsArray(internalUsers)) {
        cJSON *u;
        cJSON_ArrayForEach(u, internalUsers) {
            cJSON *jl = cJSON_GetObjectItemCaseSensitive(u, "login");
            if (cJSON_IsNumber(jl) && jl->valuedouble == (double)login)
                return 1;
        }
    }
    /* convidado? */
    if (cJSON_IsArray(guestList)) {
        cJSON *item;
        cJSON_ArrayForEach(item, guestList) {
            if (cJSON_IsNumber(item) && item->valuedouble == (double)login)
                return 2;
        }
    }
    /* senão, externo */
    return 3;
}
