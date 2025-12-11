from src.Incidencia import Incidencia


class IncidenciaVoltaje(Incidencia):
    def __init__(self, dispositivo_id, hora, voltaje_leido, diferencia):
        super().__init__(dispositivo_id, hora)
        self.voltaje = voltaje_leido
        self.diferencia = diferencia

    def describir_problema(self):
        return f"FALLO ELÉCTRICO - Salto brusco de {self.diferencia:.2f}V (Lectura: {self.voltaje}V)."

