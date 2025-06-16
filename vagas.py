#XXX: SUGESTAO DA SOFIA
#XXX: TRANSFORMAR EM CLASSE

class Vaga:
    def __init__(self, id):
        self.id = id
        self.estado = 0  # 0 = vaga livre

    def estaLivre(self):
        return self.estado == 0

    def estaOcupadaPor(self, login):
        return self.estado == login

    def ocupar(self, login):
        if self.estaLivre():
            self.estado = login
            return True
        return False

    def liberar(self):
        self.estado = 0

    def status(self):
        if self.estaLivre():
            return f"Vaga {self.id:02d}: Livre"
        return f"Vaga {self.id:02d}: Ocupada por {self.estado}"