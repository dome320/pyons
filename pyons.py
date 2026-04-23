from abc import ABC, abstractmethod


class Individual(ABC):
    @abstractmethod
    def to_genome(self) -> list:
        pass

    @abstractmethod
    def from_genome(self, genome: list) -> 'Individual': 
        pass

    def to_dict(self) -> dict:
        raise NotImplementedError()

    def from_dict(self) -> 'Individual': 
        raise NotImplementedError()

