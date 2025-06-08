// usuario.h
#ifndef USUARIO_H
#define USUARIO_H

#include <stdbool.h>

#define MAX_LOGIN_LEN 64
#define MAX_SENHA_LEN 64

typedef enum {
    INTERNO   = 1,
    CONVIDADO = 2,
    EXTERNO   = 3
} TipoUsuario;

typedef struct {
    char login[MAX_LOGIN_LEN];
    char senha[MAX_SENHA_LEN];
    TipoUsuario tipo;
} Usuario;

// Cria usuário interno (matrícula e senha).
// - Verifica formato e unicidade do login.
// - Persiste no users.csv.
// - Retorna ponteiro alocado em heap (ou NULL em erro).
Usuario* criaInterno(const char* mtr, const char* senha);

// Cria usuário convidado (CPF e senha).
// - Verifica se CPF está em guests.csv.
// - Persiste no users.csv.
// - Retorna ponteiro alocado em heap (ou NULL em erro).
Usuario* criaConvidado(const char* cpf, const char* senha);

// Retorna o tipo do usuário lido em users.csv:
// 1 = interno, 2 = convidado, 3 = externo (não encontrado).
TipoUsuario getTipo(const char* login);

#endif // USUARIO_H
