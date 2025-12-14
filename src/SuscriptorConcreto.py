from Usuario import Usuario

class SubscriptorConcreto(Usuario):
    def __init__(self, nombre, interes="TODO"):
        self.nombre = nombre
        self.interes = interes

    def update(self, incidencia):

        print(f"DEBUG: {self.nombre} ha sido notificado de {incidencia}")