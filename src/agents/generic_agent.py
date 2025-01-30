from abc import abstractmethod

from reasoners.generic_reasoner import GenericReasoner


class GenericAgent:
    def __init__(self, reasoner: GenericReasoner):
        self.reasoner = reasoner
        pass

    @abstractmethod
    def start(self):
        pass
