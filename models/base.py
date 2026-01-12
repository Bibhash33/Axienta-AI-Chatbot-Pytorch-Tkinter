from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def forward(self, inputs):
        pass