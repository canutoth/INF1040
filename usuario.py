import csv

usuarios = []
convidados = []

class Usuario:
    def __init__(self, login, senha, tipo):
        self.login = login
        self.senha = senha
        self.tipo = tipo

    #TODO: confirmar se pode ser aqui, ou se tem que ser fora da classe
    #XXX: deixa de ser necessário
    # def getLogin(self):
    #     return self.login
    
    # def getTipo(self):
    #     return self.tipo

# Verifica se o login (matrícula) tem exatamente 8 dígitos numéricos
def validaLogin(login):
    if len(login) == 7 and login.isdigit():
        return True
    return False

# Verifica se já existe um login igual em usuarios
def loginExiste(login):
    for user in usuarios:
        if user.login == login:
            return True
    return False

# Verifica se o CPF consta na lista de convidados do dia
def cpfConvidadoValido(cpf):
    for convidado in convidados:
        if convidado.login == cpf:
            return True
    return False

"""
Nome: criaInterno(login, senha)

Objetivo:
   - Registrar um novo usuário do tipo INTERNO, validando matrícula (login) e evitando duplicidade.

Acoplamento:
   - login: string contendo 8 dígitos numéricos da matrícula.
   - senha: string não vazia representando a senha.
   - retorno: None — a função não retorna valor explícito; em caso de sucesso, insere (login, senha, 1) na lista global usuarios; em caso de cancelamento (digitar "0"), não modifica a lista.

Condições de Acoplamento:
   AE: login deve ser string não vazia composta por exatamente 8 dígitos numéricos.
   AE: senha deve ser string não vazia.
   AE: usuarios deve ser uma lista de tuplas (login, senha, tipo) onde tipo é 1 (INTERNO), 2 (CONVIDADO) ou 3 (EXTERNO).
   AS: Se bem-sucedido, a tupla (login, senha, 1) é adicionada ao final de usuarios.
   AS: Se o usuário digitar "0" em qualquer prompt, a lista usuarios permanece inalterada.

Descrição:
   1) Receber login e senha.
   2)Enquanto validaLogin(login) for False: exibir mensagem de erro e solicitar novo login ou "0" para cancelar.
   3) Se o usuário digitar "0" no passo anterior, abortar e retornar.
   4) Enquanto loginExiste(login, usuarios) for True: exibir aviso de login duplicado e solicitar novo login ou "0".
   5) Se o usuário digitar "0" no passo anterior, abortar e retornar.
   6) Ao final da validação, invocar usuarios.append((login, senha, 1)) para registrar o novo usuário interno.

Hipóteses:
   - A função validaLogin verifica corretamente a formatação de matrícula.
   - A função loginExiste detecta duplicidade em usuarios.
   - O tipo 1 corresponde sempre a INTERNO.

Restrições:
   - Matrícula fixa em 8 dígitos numéricas; sem hífens ou pontos.
"""

#TODO: alterar .csv de users e guests pra ter menos coisas e passar a usar essas funções pra criar e mostrar a persistência de dados pedida
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
Nome: criaConvidado(cpf, senha)

Objetivo:
   - Registrar um novo usuário convidado para uso único.

Acoplamento:
   - cpf: str — CPF (11 dígitos numéricos) do convidado a ser criado.
   - senha: str — senha de acesso do convidado.
   - retorno: None — a função não retorna valor explícito; em caso de sucesso, insere (cpf, senha, 2) na lista global usuarios; em caso de cancelamento (digitar "0"), não altera a lista.

Condições de Acoplamento:
   AE: cpf deve ser string não vazia composta por exatamente 11 dígitos numéricos.
   AE: senha deve ser string não vazia.   AS: retorna Usuario* válido alocado em heap com campos login=cpf, senha e tipo=CONVIDADO.
   AS: Se bem-sucedido, a tupla (cpf, senha, 2) é adicionada ao final de usuarios.
   AS: Se o usuário digitar "0" em qualquer prompt, a lista usuarios permanece inalterada.

Descrição:
   1) Receber cpf e senha.
   2) Enquanto !cpfConvidadoValido(cpf): exibir mensagem de erro e solicitar novo cpf ou "0" para cancelar.
   3) Se o usuário digitar "0" no passo anterior, abortar e retornar.
   4) Enquanto loginExiste(cpf, usuarios): exibir aviso de CPF duplicado e solicitar novo cpf ou "0" para cancelar.
   5) Se o usuário digitar "0" no passo anterior, abortar e retornar.
   6) Ao final da validação, invocar usuarios.append((cpf, senha, 2)) para registrar o novo convidado.

Hipóteses:
   -  função cpfConvidadoValido verifica corretamente o formato e autorização do CPF.
   - A função loginExiste detecta duplicidade em usuarios.
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

def listarUsuarios():
    return usuarios[:]

def buscarUsuario(login):
    for u in usuarios:
        if u.login == login:
            return u
    return None