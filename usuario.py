global usuarios, convidados
usuarios = []
convidados = []

class Usuario:
    def __init__(self, login, senha, tipo):
        self.login = login
        self.senha = senha
        self.tipo = tipo

    #TODO: confirmar se pode ser aqui, ou se tem que ser fora da classe
    def getLogin(self):
        return self.login
    
    def getTipo(self):
        return self.tipo

# Verifica se o login (matrícula) tem exatamente 8 dígitos numéricos
def validaLogin(login):
    if len(login) == 8 and login.isdigit():
        return True
    return False

# Verifica se já existe um login igual em usuarios
def loginExiste(login, usuarios):
    for user, _, _ in usuarios:
        if user == login:
            return True
    return False

# Verifica se o CPF consta na lista de convidados do dia
def cpfConvidadoValido(cpf, convidados):
    for convidado in convidados:
        if convidado == cpf:
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
def criaInterno(login, senha):
    # PASSO 1: validar formato da matrícula
    while not validaLogin(login):
        # AE: login inválido
        print("Login inválido. Deve ter exatamente 8 dígitos numéricos.")
        login = input("Digite o login (matrícula) ou 0 para voltar ao menu principal: ")
        if login == "0":
            # AS: aborta sem alterar usuarios
            return

    # PASSO 2: verificar duplicidade de login
    while loginExiste(login, usuarios):
        # AE: login já cadastrado
        print("Login já existe.")
        login = input("Digite o login (matrícula) ou 0 para voltar ao menu principal: ")
        if login == "0":
            # AS: aborta sem alterar usuarios
            return

    # PASSO 3: registrar usuário interno
    usuario = Usuario(login, senha, 1)
    usuarios.append(usuario)
    # AS: usuarios atualizado com novo registro (login, senha, tipo=1)

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

def criaConvidado(cpf, senha):
    # PASSO 1: validar CPF de convidado
    while not cpfConvidadoValido(cpf):
        # AE: CPF não autorizado ou formato inválido
        print("CPF inválido ou não autorizado para convidado hoje.")
        cpf = input("Digite o CPF (11 dígitos) ou 0 para voltar ao menu principal: ")
        if cpf == "0":
            # AS: aborta sem alterar usuarios
            return

    # PASSO 2: verificar duplicidade de CPF
    while loginExiste(cpf, usuarios):
        # AE: CPF já cadastrado
        print("CPF já existe.")
        cpf = input("Digite o CPF (11 dígitos) ou 0 para voltar ao menu principal: ")
        if cpf == "0":
            # AS: aborta sem alterar usuarios
            return

    # PASSO 3: registrar usuário convidado
    usuario = Usuario(cpf, senha, 2)
    usuarios.append(usuario)
    # AS: usuarios atualizado com novo registro (cpf, senha, tipo=2)