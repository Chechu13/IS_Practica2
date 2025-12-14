class GestorSuscripciones:
    def __init__(self):
        self.subscriptores = []

    def suscribir(self, usuario):
        self.subscriptores.append(usuario)

    def desuscribir(self, usuario):
        self.subscriptores.remove(usuario)

    def notificar_suscriptores(self, incidencia):
        for sub in self.subscriptores:
            sub.update(incidencia)