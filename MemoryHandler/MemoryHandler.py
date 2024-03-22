from abc import ABC, abstractmethod

class MemoryHandler(ABC):
    @abstractmethod
    def check_available_space(self):
        pass