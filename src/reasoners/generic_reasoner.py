from abc import abstractmethod


class GenericReasoner:
    def __init__(self):
        pass

    @abstractmethod
    def process_request(self, request):
        pass
