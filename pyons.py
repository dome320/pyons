from abc import ABC, abstractmethod


class Individual(ABC):

    @abstractmethod
    def to_genome(self) -> list:
        pass
    
    @abstractmethod
    def from_genome(self) -> 'Individual': 
        pass

    def to_dict(self) -> dict:
        pass

    def from_dict(self) -> 'Individual': 
        pass
