from abc import ABC, abstractmethod


class Algorithm(ABC):
    pauseLambda = lambda: None

    @abstractmethod
    def nextIteration(self):
        pass

    def iterate(self):
        while self.nextIteration():
            self.pauseLambda