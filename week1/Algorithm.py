from abc import ABC, abstractmethod

class Algorithm(ABC):

    pauseMethod = lambda: None

    @abstractmethod
    def nextIteration(self):
        pass

    @abstractmethod
    def hasNextIteration(self):
        pass

    def iterate(self):
        while self.hasNextIteration():
            self.nextIteration()
            self.pauseMethod()
