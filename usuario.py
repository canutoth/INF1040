import csv

usuarios = []
convidados = []

"""
    Nome: Usuario(login, senha, tipo)

    Objetivo:
        Representar um usuário do sistema.

    Atributos:
        - login: str — identificador único (matrícula de 7 dígitos ou CPF).
        - senha: str — credencial de acesso.
        - tipo : int — 1=INTERNO, 2=CONVIDADO, 3=EXTERNO.
    """
class Usuario:
    def __init__(self, login, senha, tipo):
        self.login = login
        self.senha = senha
        self.tipo = tipo

"""
    Nome: validaLogin(login)

    Objetivo:
        Checar se a matrícula interna atende ao formato exigido.

    Acoplamento:
        - login: str — entrada a validar.
        - retorno: bool.

    Condições de Acoplamento:
        AE: login string (pode estar vazia).
        AS: True se login possui exatamente 7 dígitos numéricos, False caso
            contrário.

    Descrição:
        len(login)==7 e login.isdigit().

    Hipóteses:
        - Matrícula definida pela instituição em 7 dígitos.
    """
def validaLogin(login):
    if len(login) == 7 and login.isdigit():
        return True
    return False

"""
    Nome: loginExiste(login)

    Objetivo:
        Verificar duplicidade de login em `usuarios`.

    Acoplamento:
        - login: str.
        - retorno: bool.

    Descrição:
        Percorre lista global `usuarios` e compara atributo .login.
    """
def loginExiste(login):
    for user in usuarios:
        if user.login == login:
            return True
    return False

"""
    Nome: cpfConvidadoValido(cpf)

    Objetivo:
        Confirmar se o CPF consta na lista diária de convidados.

    Acoplamento:
        - cpf: str (11 dígitos).
        - retorno: bool.

    Descrição:
        Busca em lista global `convidados` (objetos Usuario, tipo 2).
    """
def cpfConvidadoValido(cpf):
    for convidado in convidados:
        if convidado.login == cpf:
            return True
    return False

"""
    Nome: criaInterno()

    Objetivo:
        Cadastrar usuário interno (tipo 1) com validação de matrícula
        exclusiva e senha não vazia.

    Fluxo resumido:
        • Solicita matrícula até válida/única ou "0" para cancelar.
        • Solicita senha (não vazia).
        • Adiciona objeto Usuario(login, senha, 1) à lista global `usuarios`.
    """
def criaInterno():
    while True:
        login = input("Digite o login (matrícula) ou 0 para voltar: ").strip()
        if login == "0":
            return # cancelamento

        if not validaLogin(login):
            print("❌ Matrícula deve ter exatamente 7 dígitos numéricos.")
            continue 

        if loginExiste(login):
            print("❌ Matrícula já cadastrada. Use a opção 1) Login.")
            continue

        break # passou nas duas validações

    senha = input("Crie sua senha: ").strip()
    if not senha:
        print("❌ Senha não pode ser vazia.")
        return

    usuarios.append(Usuario(login, senha, 1))
    print("✅ Usuário interno criado com sucesso.")

"""
    Nome: criaConvidado()

    Objetivo:
        Registrar convidado (tipo 2) de uso único, validando CPF, lista diária
        e inexistência prévia.

    Fluxo resumido:
        1) Ler CPF (ou "0" para cancelar) e verificar:
           • 11 dígitos numéricos
           • constar em `convidados` do dia (cpfConvidadoValido)
           • não estar cadastrado (ou explicar situação caso esteja)
        2) Ler senha não vazia.
        3) Criar Usuario(cpf, senha, 2) e adicionar a `usuarios` (+`convidados`).

    Observação:
        Se CPF já for convidado ➜ orienta a usar credenciais enviadas.
        Se CPF pertencer a usuário interno ➜ pede para fazer login.
    """
def criaConvidado():
    while True:
        cpf = input("Digite o CPF (11 dígitos) ou 0 para voltar: ").strip()
        if cpf == "0":
            return # cancelamento

        if len(cpf) != 11 or not cpf.isdigit():
            print("❌ CPF deve ter 11 dígitos numéricos.")
            continue

        if not cpfConvidadoValido(cpf):
            print("❌ CPF não está na lista de convidados para hoje.")
            continue

        existente = buscarUsuario(cpf)
        if existente:
            if existente.tipo == 2: # já é convidado
                print("ℹ️  Este CPF já recebeu um acesso de uso único.")
                print("    Verifique seu e-mail: o login e a senha já foram enviados.")
            else: # é usuário permanente
                print("❌ CPF pertence a usuário interno. Use a opção 1) Login.")
            return # em ambos os casos não cria de novo
        break # CPF autorizado e não usado ainda

    senha = input("Crie sua senha: ").strip()
    if not senha:
        print("❌ Senha não pode ser vazia.")
        return

    usuarios.append(Usuario(cpf, senha, 2))
    print("✅ Usuário convidado criado com sucesso.")

"""
    Nome: carregarUsuarios(caminho, tipo_padrao=None)

    Objetivo:
        Popular listas globais `usuarios` e `convidados` a partir de um CSV.

    Acoplamento:
        - caminho: str — arquivo CSV separado por vírgula.
        - tipo_padrao: int|None — se linha não contiver coluna tipo, usar este
          valor (útil para guests.csv).

    Formato esperado:
        login,senha,tipo   (tipo opcional se `tipo_padrao` fornecido)

    Descrição:
        Para cada linha válida cria objeto Usuario e adiciona às listas.
    """
def carregarUsuarios(caminho, tipo_padrao=None):
    try:
        with open(caminho, newline='', encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if not row:
                    continue
                login = row[0].strip() if len(row) > 0 else ""
                senha = row[1].strip() if len(row) > 1 else ""
                try:
                    tipo = int(row[2]) if len(row) > 2 else tipo_padrao
                except ValueError:
                    tipo = tipo_padrao

                if login and senha and tipo is not None:
                    u = Usuario(login, senha, tipo)
                    if tipo == 2:
                        convidados.append(u)
                    usuarios.append(u)
    except FileNotFoundError:
        pass

"""
    Nome: salvarUsuarios(caminho_usuarios, caminho_convidados)

    Objetivo:
        Persistir listas globais em dois CSVs distintos (usuários permanentes e
        convidados).

    Descrição:
        1) Filtra lista `usuarios` removendo objetos presentes em `convidados`.
        2) Grava CSV de permanentes e CSV de convidados (login,senha,tipo).
    """
def salvarUsuarios(caminho_usuarios, caminho_convidados):
    somente_usuarios = [u for u in usuarios if u not in convidados]

    with open(caminho_usuarios, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        for u in somente_usuarios:
            writer.writerow([u.login, u.senha, u.tipo])

    with open(caminho_convidados, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        for u in convidados:
            writer.writerow([u.login, u.senha, u.tipo])

"""
    Nome: listarUsuarios()

    Objetivo:
        Devolver *shallow copy* da lista de usuários para uso externo.

    Retorno:
        list[Usuario].
    """
def listarUsuarios():
    return usuarios[:]

"""
    Nome: buscarUsuario(login)

    Objetivo:
        Encontrar e retornar o objeto Usuario cujo .login == login.

    Retorno:
        Usuario | None.
    """
def buscarUsuario(login):
    for u in usuarios:
        if u.login == login:
            return u
    return None