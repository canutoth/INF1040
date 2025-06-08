#include <stdio.h>
#include "login.h"

/* users vem de main.c, que deve fazer:
 *
 *   cJSON *root  = cJSON_Parse(json_text);
 *   users = cJSON_GetObjectItemCaseSensitive(root, "users");
 *   // e daí chamar autentica(...)
 *
 */
cJSON *users = NULL;

int autentica(int login, int senha) {
    if (login <= 0 || senha <= 0) {
        return AUTH_INVALID_FIELDS;
    }
    if (!users || !cJSON_IsArray(users)) {
        return AUTH_NO_SUCH_LOGIN;
    }

    cJSON *u;
    cJSON_ArrayForEach(u, users) {
        cJSON *jl = cJSON_GetObjectItemCaseSensitive(u, "login");
        cJSON *js = cJSON_GetObjectItemCaseSensitive(u, "senha");
        if (cJSON_IsNumber(jl) && jl->valueint == login) {
            /* login existe */
            if (cJSON_IsNumber(js) && js->valueint == senha) {
                return AUTH_SUCCESS;
            } else {
                return AUTH_WRONG_PASSWORD;
            }
        }
    }

    return AUTH_NO_SUCH_LOGIN;
}
