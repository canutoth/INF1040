#- a lista convidados entra na usuários no inicio da aplicação (pq ai a autentica funciona pra autenticar ambos os logins)
def acoplaConvidados():
    global usuarios, convidados
    for convidado in convidados:
        usuarios.append(convidado)

#- os convidados acoplados saem da lista de usuarios no final da aplicacao
def desacoplaConvidados():
    global usuarios, convidados
    for usuario in usuarios:
        if usuario not in convidados:
            convidados.append(usuario)
    usuarios = [usuario for usuario in usuarios if usuario not in convidados]