"""
Nome: OcupaVaga(vaga_id, est, usuario_login)

Objetivo: tentar ocupar uma vaga específica com o login do usuário.

Acoplamento:
    vaga_id: int — ID da vaga desejada.
    est: Estacionamento — estacionamento onde a vaga está.
    usuario_login: str — login do usuário que ocupa a vaga.

Condições de acoplamento:
    AE: vaga_id é inteiro válido.
    AE: est contém a vaga informada.
    AS: vaga marcada como ocupada no estacionamento (se livre).

Descrição:
    1) Procura a vaga pelo ID.
    2) Se vaga livre, ocupa e salva estado.
    3) Se ocupada, informa o usuário ocupante.
    4) Se ID inválido, exibe erro.

Hipóteses:
    - O estado das vagas pode ser salvo corretamente.

"""

def OcupaVaga(vaga_id, est, usuario_login):
    for idx, (id_vaga, status) in enumerate(est.vagas):
        if id_vaga == vaga_id:
            if status == "0":
                est.vagas[idx] = (id_vaga, usuario_login)
                est.salvar_vagas()
                print(f"Vaga {vaga_id} ocupada por {usuario_login}.")
                return 0
            else:
                print(f"Vaga {vaga_id} já está ocupada por {status}.")
                return -1
    print("ID de vaga inválido.")
    return -1

"""
Nome: LiberarVaga(usuario_login, est)

Objetivo:
    Liberar a vaga ocupada por um usuário específico no estacionamento.

Acoplamento:
    usuario_login: str — identificador do usuário que ocupa a vaga.
    est: Estacionamento — objeto representando o estacionamento onde a vaga está.

Condições de acoplamento:
    AE: usuário está ocupando uma vaga no estacionamento.
    AS: vaga é marcada como livre e o estado do estacionamento é salvo.

Descrição:
    1) Percorrer a lista de vagas do estacionamento.
    2) Identificar a vaga cujo status corresponde ao usuario_login.
    3) Se encontrada, marcar a vaga como livre ("0") e salvar o estado.
    4) Se nenhuma vaga estiver ocupada pelo usuário, exibir mensagem de erro.

Hipóteses:
    - O método salvar_vagas do objeto estacionamento funciona corretamente.
    - O usuário_login é uma string válida e corresponde a um usuário existente.
"""

def LiberarVaga(usuario_login, est):
    for idx, (id_vaga, status) in enumerate(est.vagas):
        if status == usuario_login:
            est.vagas[idx] = (id_vaga, "0")
            est.salvar_vagas()
            print(f"Vaga {id_vaga} liberada para o usuário {usuario_login}.")
            return 0
    print(f"Nenhuma vaga ocupada pelo usuário {usuario_login}.")
    return -1

"""Nome: VerificarStatus(vaga_id, est)

Objetivo: exibir o status de uma vaga específica.

Acoplamento:
    vaga_id: int — ID da vaga.
    est: Estacionamento — estacionamento onde está a vaga.

Condições de acoplamento:
    AE: vaga_id existe no estacionamento.
    AS: exibe se a vaga está livre ou ocupada (e por quem).

Descrição:
    1) Procura a vaga pelo ID.
    2) Exibe o status correspondente.
    3) Se não existe, exibe erro.

Hipóteses:
    - O estado das vagas está correto na memória.
"""

def VerificarStatus(vaga_id, est):
    for id_vaga, status in est.vagas:
        if id_vaga == vaga_id:
            if status == "0":
                print(f"Vaga {vaga_id}: Livre.")
            else:
                print(f"Vaga {vaga_id}: Ocupada por {status}.")
            return
    print("ID de vaga inválido.")
