
"""
Nome: autentica(login, senha)

Objetivo: validar as credenciais do usuário (login e senha) com base na base de dados de usuários.

Acoplamento:
    login: str — nome de usuário a ser autenticado.
    senha: str — senha associada ao usuário.
    usuarios: list[tuple[str, str, int]] — lista de tuplas contendo (login, senha, tipo_usuario) onde tipo_usuario pode ser 1 (INTERNO), 2 (CONVIDADO) ou 3 (EXTERNO).
    bool — True se as credenciais corresponderem a um usuário da lista, False caso contrário.

Condições de acoplamento:
    AE: login deve ser uma string não vazia.
    AE: senha deve ser uma string não vazia.
    AE: usuarios deve ser uma lista de tuplas (str, str, int), não vazia e com tipo_usuario em {1,2,3}.
    AS: informa se o login é válido/inválido.
    AS: informa se a senha corresponde à senha do usuário com aquele login.
    AS: retorna True se o login e senha forem válidos e correspondentes a um usuário na lista.

Descrição:
    1) Receber login, senha e lista usuarios.
    2) Percorrer cada tupla (user, pwd, tipo) em usuarios.
    3) Em cada iteração, comparar user == login e pwd == senha.
    4) Se ambas as condições forem verdadeiras, interromper a busca e retornar True.
    5) Se a lista for percorrida sem encontrar correspondência, retornar False.

Hipóteses:
    - A base de dados de usuários está ativa e acessível.
    - O sistema onde a função é executada possui permissões para consultar os dados de autenticação.
"""

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

def autentica(login, senha, lista_usuarios):
    for user in lista_usuarios:
        if user.login == login and user.senha == senha:
            return user
    return None