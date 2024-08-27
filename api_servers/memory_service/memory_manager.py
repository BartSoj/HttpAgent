class MemoryManager:

    def __init__(self):
        self.memory_table = []

    def get_memory(self):
        return self.memory_table

    def save_memory(self, memory):
        self.memory_table.append(memory)

    def close(self):
        del self.memory_table
