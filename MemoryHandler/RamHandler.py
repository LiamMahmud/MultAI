from MemoryHandler import MemoryHandler

class RamHandler(MemoryHandler):
    def __init__(self, available_space):
        self.available_space = available_space

    def check_available_space(self):
        print("Checking RAM space...")
        if self.available_space >= 1024:  # Assuming available space is in MB
            return True
        else:
            return False