class Dispositivo:
    def __init__(self, id_dispositivo):
        self.id = id_dispositivo

    def __str__(self):
        return f"Sensor de Vía #{self.id}"

    def get_identificador_completo(self):
        """Método de negocio para identificar inequívocamente el hardware"""
        return f"DISP-{self.id:04d}"