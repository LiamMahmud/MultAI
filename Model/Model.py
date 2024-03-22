import os
from MemoryHandler.VRamHandler import VRamHandler
from MemoryHandler.RamHandler import RamHandler
class Model:
    def __init__(self, model_name: str, model_path: str, device: str):
        self.model_name = model_name
        self.model_path = model_path
        self.device = device

    def Load_Model(self): # Add model loading model for each model
        print(f"Loading Model into {self.device}...")

    def Unload_Model(self): # maybe let this logic to memory handlers
        print(f"Unloading Model...")


model = Model(model_name="Mistral" ,model_path="./home", device="GPU")
print(os.environ)