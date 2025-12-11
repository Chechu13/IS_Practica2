from abc import ABC, abstractmethod

class Incidencia(ABC):
    def __init__(self, dispositivo_id, hora):
        self.dispositivoAfectado = dispositivo_id
        self.hora = hora

    @abstractmethod
    def describir_problema(self):
        pass

    def __str__(self):
        return f"[{self.hora}] Dispositivo {self.dispositivoAfectado}: {self.describir_problema()}"
