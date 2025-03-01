from dotenv import load_dotenv
import os
import openai

load_dotenv()


class OpenAIClient:
    _instance = None

    def __init__(self):
        self.client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls._instance.client = None
        return cls._instance

    def initialize(self):
        if self.client is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set")
            openai.api_key = api_key
            self.client = openai.Client(api_key=api_key)

    def get_client(self):
        if self.client is None:
            self.initialize()
        return self.client
