#include <stdio.h>
#include "login.h"

int main(void) {
    int código = autentica(12345678, 4321);
    switch (código) {
        case AUTH_SUCCESS:        printf("Login OK\n");          break;
        case AUTH_NO_SUCH_LOGIN:  printf("Login não existe\n");  break;
        case AUTH_WRONG_PASSWORD: printf("Senha incorreta\n");   break;
        case AUTH_INVALID_FIELDS: printf("Campos inválidos\n");  break;
    }
    return 0;
}
