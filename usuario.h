#ifndef USUARIO_H
#define USUARIO_H

#include "cJSON.h"

/* Estrutura retornada em caso de sucesso */
typedef struct {
    long long login;  /* matrícula (interno) ou CPF (convidado/externo) */
    int senha;
    int tipo;         /* 1=interno, 2=convidado, 3=externo */
} Usuario;

/* Os ponteiros abaixo devem ser definidos em main.c */
extern cJSON *internalUsers;  /* array cJSON* de objetos {login,senha,...} */
extern cJSON *guestList;      /* array cJSON* de números (CPFs) */

/* Cria um usuário interno; retorna NULL e imprime erro em stderr */
Usuario *criaInterno(long long mtr, int senha);

/* Cria um usuário convidado (uso único); retorna NULL + erro em stderr */
Usuario *criaConvidado(long long cpf, int senha);

/* Classifica tipo pelo “login” (matrícula/CPF) */
int getTipo(long long login);

#endif /* USUARIO_H */
