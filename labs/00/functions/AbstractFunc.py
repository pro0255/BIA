from abc import ABC, abstractmethod


class AbstractFunc(ABC):
    @abstractmethod
    def run(self, vector):
        print("Running method")
