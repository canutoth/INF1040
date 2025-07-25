import csv

usuarios = []
convidados = []

# ---------------------------------------------------------------------------
# FUNCOES INTERNAS
"""
    Nome: novo_usuario(login, senha, tipo)

    Objetivo:
        Criar e retornar o dicionário-usuário no padrão único do sistema.

    Retorno:
        dict {"login": str, "senha": str, "tipo": int}
"""
def _novo_usuario(login: str, senha: str, tipo: int) -> dict:
    """Cria e devolve o dicionário-usuário."""
    return {"login": login, "senha": senha, "tipo": tipo}

"""
    Nome: validaLogin(login)

    Objetivo:
       - Verificar se a matrícula interna possui formato correto (7 dígitos).

    Acoplamento:
       - login: str — matrícula digitada.
       - retorno: bool — True se válido, False caso contrário.

    Condições de Acoplamento:
       AE: login string (possivelmente vazia).
       AS: retorna True se len(login)==7 e login.isdigit().

    Descrição:
       1) Checa comprimento e composição numérica.

    Hipóteses:
       - Matrícula institucional sempre tem 7 dígitos numéricos.

    Restrições:
       - Nenhuma.
"""
def _validaLogin(login: str) -> bool:
    """Retorna True se matrícula tem 7 dígitos numéricos."""
    return len(login) == 7 and login.isdigit()

"""
    Nome: loginExiste(login)

    Objetivo:
       - Detectar duplicidade de login na lista global `usuarios`.

    Acoplamento:
       - login: str — identificador a verificar.
       - retorno: bool — True se duplicado, False se único.

    Condições de Acoplamento:
       AE: lista `usuarios` pode estar vazia.
       AS: percorre `usuarios` sem alterá-la.

    Descrição:
       1) Itera sobre `usuarios` comparando u["login"] com login.

    Hipóteses:
       - `usuarios` contém somente dicionários no formato estabelecido.

    Restrições:
       - Custo O(n) onde n = len(usuarios).
    """
def _loginExiste(login: str) -> bool:
    """Verifica duplicidade em `usuarios`."""
    return any(u["login"] == login for u in usuarios)

"""
    Nome: cpfConvidadoValido(cpf)

    Objetivo:
       - Verificar se um CPF consta na lista diária de convidados.

    Acoplamento:
       - cpf: str — CPF de 11 dígitos.
       - retorno: bool.

    Condições de Acoplamento:
       AE: cpf string de 11 dígitos.
       AS: percorre `convidados` sem modificá-lo.

    Descrição:
       1) Procura cpf em convidado["login"] para cada item da lista.

    Hipóteses:
       - `convidados` contém apenas usuários de tipo 2.

    Restrições:
       - Tempo O(m) onde m = len(convidados).
    """
def _cpfConvidadoValido(cpf: str) -> bool:
    """Checa se CPF está na lista diária de convidados."""
    return any(c["login"] == cpf for c in convidados)

"""
    Nome: buscarUsuario(login)

    Objetivo:
       - Retornar o registro de usuário cujo login corresponde ao parâmetro.

    Acoplamento:
       - login: str.
       - retorno: dict | None.

    Condições de Acoplamento:
       AE: lista `usuarios` inicializada.
       AS: não altera listas globais.

    Descrição:
       1) Itera sobre `usuarios`; devolve primeiro match ou None.

    Hipóteses:
       - Logins são únicos em `usuarios`.

    Restrições:
       - Busca linear.
    """
def _buscarUsuario(login: str):
    """Retorna dicionário-usuário ou None."""
    return next((u for u in usuarios if u["login"] == login), None)
# ---------------------------------------------------------------------------
# APIs Publicas
def novo_usuario(login: str, senha: str, tipo: int) -> dict:
    return _novo_usuario(login, senha, tipo)

def validaLogin(login: str) -> bool:
    return _validaLogin(login)

def loginExiste(login: str) -> bool:
    return _loginExiste(login)

def cpfConvidadoValido(cpf: str) -> bool:
    return _cpfConvidadoValido(cpf)

def buscarUsuario(login: str):
    return _buscarUsuario(login)

"""
    Nome: criaInterno()

    Objetivo:
       - Registrar usuário interno (tipo 1) após validações.

    Acoplamento:
       - listas globais `usuarios`.
       - input()/print() para interação CLI.
       - retorno: None (efeito colateral: adiciona usuário).

    Condições de Acoplamento:
       AE: usuário interage pelo terminal.
       AS: Em sucesso, novo registro é inserido em `usuarios`.

    Descrição:
       1) Solicita matrícula até ser válida, única ou "0" para cancelar.
       2) Solicita senha não vazia.
       3) Insere dicionário {"login":..., "senha":..., "tipo":1} em `usuarios`.

    Hipóteses:
       - O ambiente de execução suporta I/O de console.

    Restrições:
       - Loop bloqueante até entrada aceitável ou cancelamento.
    """
def criaInterno() -> None:
    while True:
        login = input("Digite o login (matrícula) ou 0 para voltar: ").strip()
        if login == "0":
            return
        if not validaLogin(login):
            print("❌ Matrícula deve ter exatamente 7 dígitos numéricos.")
            continue
        if loginExiste(login):
            print("❌ Matrícula já cadastrada. Use a opção 1) Login.")
            continue
        break

    senha = input("Crie sua senha: ").strip()
    if not senha:
        print("❌ Senha não pode ser vazia.")
        return

    usuarios.append(novo_usuario(login, senha, 1))
    print("✅ Usuário interno criado com sucesso.")

"""
    Nome: criaConvidado()

    Objetivo:
       - Registrar convidado (tipo 2) de uso único.

    Acoplamento:
       - listas globais `usuarios`, `convidados`.
       - input()/print() para interação.

    Condições de Acoplamento:
       AE: cpf string digitada pelo usuário.
       AS: adiciona novo convidado às listas ao final do fluxo.

    Descrição:
       1) Valida CPF (11 dígitos) e se está autorizado.
       2) Verifica duplicidade (interno ou já convidado).
       3) Solicita senha e cria registro tipo 2.

    Hipóteses:
       - Lista diária de convidados já populada em `convidados`.

    Restrições:
       - Loop bloqueante; cancela com "0".
    """
def criaConvidado() -> None:
    while True:
        cpf = input("Digite o CPF (11 dígitos) ou 0 para voltar: ").strip()
        if cpf == "0":
            return
        if len(cpf) != 11 or not cpf.isdigit():
            print("❌ CPF deve ter 11 dígitos numéricos.")
            continue
        if not cpfConvidadoValido(cpf):
            print("❌ CPF não está na lista de convidados para hoje.")
            continue

        existente = buscarUsuario(cpf)
        if existente:
            if existente["tipo"] == 2:
                print("ℹ️  Este CPF já recebeu acesso de uso único (veja seu e-mail).")
            else:
                print("❌ CPF pertence a usuário interno. Use a opção 1) Login.")
            return
        break

    senha = input("Crie sua senha: ").strip()
    if not senha:
        print("❌ Senha não pode ser vazia.")
        return

    novo = novo_usuario(cpf, senha, 2)
    usuarios.append(novo)
    convidados.append(novo)
    print("✅ Usuário convidado criado com sucesso.")

"""
    Nome: carregarUsuarios(caminho, tipo_padrao=None)

    Objetivo:
       - Popular `usuarios` (e `convidados`) a partir de arquivo CSV.

    Acoplamento:
       - caminho: str — arquivo CSV (login,senha,tipo).
       - tipo_padrao: int|None — valor adotado se coluna tipo ausente.

    Condições de Acoplamento:
       AE: arquivo pode não existir (tratado).
       AS: listas globais atualizadas com novos registros.

    Descrição:
       1) Abrir CSV; iterar linhas válidas.  
       2) Aplicar `tipo_padrao` quando necessário.  
       3) Criar dict via novo_usuario() e inserir-se na(s) lista(s).

    Hipóteses:
       - Arquivo usa vírgula como separador e UTF-8.

    Restrições:
       - Ignora linhas malformadas ou vazias.
    """
def carregarUsuarios(caminho: str, tipo_padrao = None) -> None:
    try:
        with open(caminho, newline='', encoding="utf-8") as f:
            for row in csv.reader(f, delimiter=','):
                if not row:
                    continue
                login = row[0].strip()
                senha = row[1].strip() if len(row) > 1 else ""
                try:
                    tipo = int(row[2]) if len(row) > 2 else tipo_padrao
                except ValueError:
                    tipo = tipo_padrao
                if login and senha and tipo is not None:
                    u = novo_usuario(login, senha, tipo)
                    if tipo == 2:
                        convidados.append(u)
                    usuarios.append(u)
    except FileNotFoundError:
        pass

"""
    Nome: salvarUsuarios(caminho_usuarios, caminho_convidados)

    Objetivo:
       - Persistir dados em dois CSVs: permanentes e convidados.

    Acoplamento:
       - caminhos dos arquivos destino.

    Condições de Acoplamento:
       AE: diretório com permissão de escrita.
       AS: arquivos sobrescritos com conteúdo atualizado.

    Descrição:
       1) Filtra `usuarios` retirando aqueles presentes em `convidados`.  
       2) Escreve permanentes no primeiro CSV.  
       3) Escreve `convidados` no segundo CSV.

    Restrições:
       - Sobrescreve arquivos sem merge incremental.
    """
def salvarUsuarios(caminho_usuarios: str, caminho_convidados: str) -> None:
    permanentes = [u for u in usuarios if u not in convidados]

    with open(caminho_usuarios, "w", newline='', encoding="utf-8") as f:
        w = csv.writer(f, delimiter=',')
        for u in permanentes:
            w.writerow([u["login"], u["senha"], u["tipo"]])

    with open(caminho_convidados, "w", newline='', encoding="utf-8") as f:
        w = csv.writer(f, delimiter=',')
        for u in convidados:
            w.writerow([u["login"], u["senha"], u["tipo"]])

"""
    Nome: autentica(login, senha)

    Objetivo:
        Validar as credenciais informadas e retornar o usuário ou código de erro.

    Acoplamento:
        - login: str — identificador digitado pelo usuário.
        - senha: str — senha digitada.
        - retorno: dict | int — dicionário usuário se sucesso, ou código de erro:
            0 = sucesso (retorna dict do usuário)
            1 = login inexistente
            2 = senha incorreta
            3 = campos inválidos

    Condições de Acoplamento:
        AE: login e senha são strings.
        AS: Retorna usuário se autenticação bem-sucedida ou código de erro.

    Descrição:
        1) Validar campos (não vazios).
        2) Verificar se login existe.
        3) Verificar se senha está correta.
        4) Retornar usuário ou código de erro apropriado.

    Hipóteses:
        - Lista de usuários reflete o catálogo válido.
        - Logins são únicos.

    Restrições:
        - Busca sequencial O(n).
"""
def autentica(login: str, senha: str):
    # Validação de campos
    if not login or not senha:
        return 3
    
    # Buscar usuário
    user = buscarUsuario(login)
    if user is None:
        return 1
    
    # Verificar senha
    if user["senha"] != senha:
        return 2
    
    return user


"""
    Nome: getLogin(usuario)

    Objetivo:
        Obter o login de um usuário sem expor a estrutura interna.

    Acoplamento:
        - usuario: dict — objeto usuário.
        - retorno: str — login do usuário.

    Condições de Acoplamento:
        AE: usuario é dict válido com chave 'login'.
        AS: retorna string do campo login.

    Descrição:
        Função de acesso que encapsula o campo "login" do usuário.

    Hipóteses:
        - usuario possui a chave 'login' obrigatória.

    Restrições:
        - Acesso direto O(1).
        - Não valida existência da chave.
"""
def getLogin(usuario: dict) -> str:
    """Retorna o login do usuário de forma encapsulada."""
    return usuario["login"]

"""
    Nome: getTipo(usuario)

    Objetivo:
        Obter o tipo de um usuário sem expor a estrutura interna.

    Acoplamento:
        - usuario: dict — objeto usuário.
        - retorno: int — tipo do usuário (1=interno, 2=convidado).

    Condições de Acoplamento:
        AE: usuario pode ser dict válido ou None.
        AS: retorna tipo inteiro ou -1 se usuario é None.

    Descrição:
        Função de acesso que encapsula o campo "tipo" do usuário.

    Hipóteses:
        - Se usuario não é None, possui chave 'tipo'.
        - Tipos válidos são inteiros positivos.

    Restrições:
        - Não valida existência da chave.
"""
def getTipo(usuario: dict) -> int:
    """Retorna o tipo do usuário de forma encapsulada."""
    if usuario is None:
        return -1
    return usuario["tipo"]

__all__ = [
    # helpers/funções de domínio
    "novo_usuario",
    "validaLogin",
    "loginExiste",
    "cpfConvidadoValido",
    "buscarUsuario",

    # operações de alto nível
    "criaInterno",
    "criaConvidado",
    "carregarUsuarios",
    "salvarUsuarios",
    "autentica",

    # getters seguros
    "getLogin",
    "getTipo",
]