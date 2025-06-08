#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"
#include "login.h"

static char *read_file(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    rewind(f);
    char *buf = malloc(len + 1);
    if (!buf) { fclose(f); return NULL; }
    if (fread(buf, 1, len, f) != (size_t)len) {
        free(buf);
        fclose(f);
        return NULL;
    }
    buf[len] = '\0';
    fclose(f);
    return buf;
}

int autentica(int login, int senha) {
    if (login <= 0 || senha <= 0) {
        return AUTH_INVALID_FIELDS;
    }

    char *json_txt = read_file("users.json");
    if (!json_txt) {
        perror("Erro ao abrir users.json");
        return AUTH_NO_SUCH_LOGIN;
    }

    cJSON *root = cJSON_Parse(json_txt);
    free(json_txt);
    if (!root) {
        fprintf(stderr, "JSON inválido\n");
        return AUTH_NO_SUCH_LOGIN;
    }

    cJSON *users = cJSON_GetObjectItemCaseSensitive(root, "users");
    if (!cJSON_IsArray(users)) {
        cJSON_Delete(root);
        fprintf(stderr, "\"users\" não é array\n");
        return AUTH_NO_SUCH_LOGIN;
    }

    int result = AUTH_NO_SUCH_LOGIN;
    cJSON *u;
    cJSON_ArrayForEach(u, users) {
        cJSON *jl = cJSON_GetObjectItemCaseSensitive(u, "login");
        cJSON *js = cJSON_GetObjectItemCaseSensitive(u, "senha");
        if (cJSON_IsNumber(jl) && jl->valueint == login) {
            /* login existe */
            if (cJSON_IsNumber(js) && js->valueint == senha) {
                result = AUTH_SUCCESS;
            } else {
                result = AUTH_WRONG_PASSWORD;
            }
            break;
        }
    }

    cJSON_Delete(root);
    return result;
}
