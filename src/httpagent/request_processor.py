class RequestProcessor:
    def __init__(self, incoming_request_processor=None, outgoing_request_processor=None):
        self.incoming_request_processor = incoming_request_processor or self.default_incoming_request_processor
        self.outgoing_request_processor = outgoing_request_processor or self.default_outgoing_request_processor

    def default_incoming_request_processor(self, request):
        return request

    def default_outgoing_request_processor(self, request):
        return request

    def process_incoming_request(self, request):
        return self.incoming_request_processor(request)

    def process_outgoing_request(self, request):
        return self.outgoing_request_processor(request)
