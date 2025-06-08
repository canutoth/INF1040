#include <stdio.h>
#include <string.h>
#include "fila.h"

#define PASS(msg) printf("[PASS] %s\n", msg)
#define FAIL(msg) printf("[FAIL] %s\n", msg)

int main(void) {
    Fila fila;

    // 1. Inicialização de uma fila vazia
    inicializarFila(&fila);
    if (fila.inicio == NULL && fila.fim == NULL && fila.tamanho == 0) {
        PASS("Inicializacao fila vazia");
    } else {
        FAIL("Inicializacao fila vazia");
    }

    // 2. Consulta em fila vazia
    int pos = consultarPosicaoNaFila(&fila, "U1");
    if (pos == -1) PASS("Consulta em fila vazia retorna -1");
    else FAIL("Consulta em fila vazia");

    // 3. Adicao na fila vazia
    int ret = adicionarNaFila(&fila, "U1", 1);
    if (ret == 0 && fila.tamanho == 1
        && strcmp(fila.inicio->id, "U1") == 0
        && strcmp(fila.fim->id, "U1") == 0) {
        PASS("Adicao na fila vazia");
    } else {
        FAIL("Adicao na fila vazia");
    }

    // 4. Consulta em fila com um elemento
    pos = consultarPosicaoNaFila(&fila, "U1");
    if (pos == 1) PASS("Consulta posicao unico elemento");
    else FAIL("Consulta posicao unico elemento");

    // 5. Consulta de usuario inexistente
    pos = consultarPosicaoNaFila(&fila, "U9");
    if (pos == -1) PASS("Consulta usuario inexistente");
    else FAIL("Consulta usuario inexistente");

    // 6. Rejeicao de duplicata
    int prevSize = fila.tamanho;
    ret = adicionarNaFila(&fila, "U1", 1);
    if (ret == -1 && fila.tamanho == prevSize) PASS("Rejeicao de duplicata");
    else FAIL("Rejeicao de duplicata");

    // 7. Consulta de posicao em multiplos elementos
    adicionarNaFila(&fila, "U2", 2);
    adicionarNaFila(&fila, "U3", 3);
    int p1 = consultarPosicaoNaFila(&fila, "U1");
    int p2 = consultarPosicaoNaFila(&fila, "U2");
    int p3 = consultarPosicaoNaFila(&fila, "U3");
    if (p1 == 1 && p2 == 2 && p3 == 3) PASS("Consulta multiplos elementos");
    else FAIL("Consulta multiplos elementos");

    // 8. Ordenacao por prioridade
    // Fila: U1(p1), U2(p2), U3(p3)
    // Vamos inverter prioridades para testar: recriar fila
    inicializarFila(&fila);
    adicionarNaFila(&fila, "U1", 3);
    adicionarNaFila(&fila, "U2", 2);
    ordenarFilaPorPrioridade(&fila);
    if (strcmp(fila.inicio->id, "U2") == 0 && strcmp(fila.fim->id, "U1") == 0) {
        PASS("Ordenacao por prioridade simples");
    } else {
        FAIL("Ordenacao por prioridade simples");
    }

    // 9. Preservacao da ordem de chegada para mesma prioridade
    inicializarFila(&fila);
    adicionarNaFila(&fila, "U1", 2);
    adicionarNaFila(&fila, "U2", 2);
    ordenarFilaPorPrioridade(&fila);
    if (strcmp(fila.inicio->id, "U1") == 0 && strcmp(fila.inicio->next->id, "U2") == 0) {
        PASS("Preservacao ordem mesma prioridade");
    } else {
        FAIL("Preservacao ordem mesma prioridade");
    }

    // 10. Ordenacao idempotente em fila vazia
    inicializarFila(&fila);
    ordenarFilaPorPrioridade(&fila);
    if (fila.inicio == NULL && fila.fim == NULL) PASS("Ordenacao idempotente fila vazia");
    else FAIL("Ordenacao idempotente fila vazia");

    // 11. Ordenacao idempotente em fila com 1 elemento
    inicializarFila(&fila);
    adicionarNaFila(&fila, "U1", 1);
    ordenarFilaPorPrioridade(&fila);
    if (fila.inicio == fila.fim && fila.tamanho == 1) PASS("Ordenacao idempotente 1 elemento");
    else FAIL("Ordenacao idempotente 1 elemento");

    // 12. Remocao de usuario inexistente
    inicializarFila(&fila);
    adicionarNaFila(&fila, "U1", 1);
    adicionarNaFila(&fila, "U2", 1);
    prevSize = fila.tamanho;
    ret = removerDaFila(&fila, "U9");
    if (ret == -1 && fila.tamanho == prevSize) PASS("Remocao usuario inexistente");
    else FAIL("Remocao usuario inexistente");

    // 13. Remocao da cabeca da fila
    inicializarFila(&fila);
    adicionarNaFila(&fila, "U1", 1);
    adicionarNaFila(&fila, "U2", 1);
    adicionarNaFila(&fila, "U3", 1);
    prevSize = fila.tamanho;
    removerDaFila(&fila, "U1");
    if (strcmp(fila.inicio->id, "U2") == 0 && fila.tamanho == prevSize - 1) {
        PASS("Remocao cabeca da fila");
    } else {
        FAIL("Remocao cabeca da fila");
    }

    // 14. Remocao da cauda da fila
    inicializarFila(&fila);
    adicionarNaFila(&fila, "U1", 1);
    adicionarNaFila(&fila, "U2", 1);
    adicionarNaFila(&fila, "U3", 1);
    prevSize = fila.tamanho;
    removerDaFila(&fila, "U3");
    if (strcmp(fila.fim->id, "U2") == 0 && fila.tamanho == prevSize - 1) {
        PASS("Remocao cauda da fila");
    } else {
        FAIL("Remocao cauda da fila");
    }

    // 15. Remocao de no intermediario da fila
    inicializarFila(&fila);
    adicionarNaFila(&fila, "U1", 1);
    adicionarNaFila(&fila, "U2", 1);
    adicionarNaFila(&fila, "U3", 1);
    prevSize = fila.tamanho;
    removerDaFila(&fila, "U2");
    if (fila.inicio->next && strcmp(fila.inicio->next->id, "U3") == 0
        && fila.tamanho == prevSize - 1) {
        PASS("Remocao no intermediario");
    } else {
        FAIL("Remocao no intermediario");
    }

    return 0;
}
