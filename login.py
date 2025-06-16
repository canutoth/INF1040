"""
    Nome: autentica(login, senha, lista_usuarios)

    Objetivo:
        Validar credenciais e devolver o objeto `Usuario` correspondente,
        permitindo que o chamador conheça o tipo e demais atributos.

    Acoplamento:
        - login: str — identificador digitado pelo usuário.
        - senha: str — senha digitada.
        - lista_usuarios: list[Usuario] — objetos com atributos
          .login, .senha, .tipo (1=INTERNO, 2=CONVIDADO, 3=EXTERNO).
        - retorno: Usuario | None — objeto autenticado ou None se falhar.

    Condições de Acoplamento:
        AE: login e senha são strings não vazias.
        AE: lista_usuarios pode estar vazia, mas seus elementos (quando
            presentes) expõem atributos .login e .senha.
        AS: Se login e senha coincidirem, devolve o objeto `Usuario`.
        AS: Caso contrário, devolve None.

    Descrição:
        1) Percorrer cada usuário em lista_usuarios.
        2) Comparar `user.login` e `user.senha` com as credenciais fornecidas.
        3) Encontrando correspondência exata, retornar o próprio objeto.
        4) Ao final da iteração sem sucesso, retornar None.

    Hipóteses:
        - A lista representa o “catalogo” em memória válido no momento da
          chamada; alterações na lista se refletem em chamadas subsequentes.
        - Para convidados (tipo 2) o login é o CPF.
        - Não há dois objetos com mesmo .login (unicidade garantida em cadastro).

    Restrições:
        - Busca sequencial O(n).
        - Não altera estado dos objetos; apenas leitura.
"""
def autentica(login, senha, lista_usuarios):
    for user in lista_usuarios:
        if user.login == login and user.senha == senha:
            return user
    return None

#XXX: SUGESTÃO DA SOFIA

#XXX: IMPORTANTE AQUI!! Alterei a função pq agora temos uma classe Usuario e uma lista de itens da classe, e não uma lista de tuplas
# def autentica(login, senha, usuarios):
#     # PASSO 1: iterar sobre cada usuário registrado
#     for user, pwd, tipo in usuarios:
#         # PASSO 2: comparar credenciais fornecidas com registro atual
#         if user == login and pwd == senha:
#             # AS: retorna True ao encontrar combinação válida
#             return True
#     # PASSO 3: nenhuma correspondência encontrada após percorrer toda a lista
#     return False
#     # AS: retorna False quando falha na autenticação