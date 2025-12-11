from src.Incidencia import Incidencia


class IncidenciaBloqueo(Incidencia):
    def __init__(self, dispositivo_id, hora, duracion_segundos):
        super().__init__(dispositivo_id, hora)
        self.duracion = duracion_segundos

    def describir_problema(self):
        return f"BLOQUEO CRÍTICO - Tren detenido durante {self.duracion} segundos."

