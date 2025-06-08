#ifndef LOGIN_H
#define LOGIN_H

#define AUTH_SUCCESS           0  /* credenciais corretas */
#define AUTH_NO_SUCH_LOGIN     1  /* login não existe */
#define AUTH_WRONG_PASSWORD    2  /* senha incorreta */
#define AUTH_INVALID_FIELDS    3  /* campos inválidos */

int autentica(int login, int senha);

#endif /* LOGIN_H */
