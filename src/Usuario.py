from abc import ABC, abstractmethod

class Usuario(ABC):
    @abstractmethod
    def update(self, incidencia):
        pass