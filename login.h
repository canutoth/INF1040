#ifndef LOGIN_H
#define LOGIN_H

#include "usuario.h"

// códigos de retorno
#define AUTH_SUCCESS       0
#define AUTH_NO_USER       1
#define AUTH_BAD_PASSWORD  2
#define AUTH_INVALID_FIELD 3

// autentica: compara login/senha em users.csv
// - login e senha não podem ser NULL ou string vazia
// - retorna um dos códigos acima
int autentica(const char *login, const char *senha, Usuario* usuarios, int totalUsuarios);

#endif // LOGIN_H
