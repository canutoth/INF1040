"""
Nome: autentica(login, senha, lista_usuarios)

Objetivo:
    Validar as credenciais informadas e devolver o **dicionário-usuário**
    correspondente, permitindo ao chamador acessar login, senha e tipo.

Acoplamento:
    - login: str — identificador digitado pelo usuário.
    - senha: str — senha digitada.
    - lista_usuarios: list[dict] — cada dict tem chaves
        'login', 'senha', 'tipo' (1=INTERNO, 2=CONVIDADO, 3=EXTERNO).
    - retorno: dict | None — dicionário autenticado ou None se falhar.

Condições de Acoplamento:
    AE: login e senha são strings não vazias.
    AE: lista_usuarios pode estar vazia; seus elementos possuem as chaves acima.
    AS: Se login e senha coincidirem, devolve o próprio dict.
    AS: Caso contrário, devolve None.

Descrição:
    1) Percorrer cada usuário em lista_usuarios.
    2) Comparar user['login'] e user['senha'] com os parâmetros.
    3) Encontrando correspondência exata, retornar o dicionário.
    4) Ao final da iteração sem sucesso, retornar None.

Hipóteses:
    - A lista reflete o catálogo válido no momento da chamada.
    - Não há dois usuários com o mesmo 'login' (unicidade garantida em cadastro).

Restrições:
    - Busca sequencial O(n).
    - Não altera estado dos dicionários; apenas leitura.
"""
def autentica(login: str, senha: str, lista_usuarios: list[dict]):
    for user in lista_usuarios:
        if user["login"] == login and user["senha"] == senha:
            return user
    return None