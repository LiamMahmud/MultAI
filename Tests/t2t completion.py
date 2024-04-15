from ctransformers import AutoModelForCausalLM
import time
from ctransformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline

llm = AutoModelForCausalLM.from_pretrained("../ModelFiles/Chat/Mistral-7b/mistral-7b-instruct-v0.2.Q5_K_M.gguf",
                                           model_type="mistral",
                                           gpu_layers=32)

start = time.time()

chars = 0
args = {
    "prompt": "WHat is a large language model",
    "stream": True
}

for chunk in llm(**args):
    print(chunk, end="")
    chars += len(chunk)

end = time.time()
print("Time taken: ", end-start)
print("chars per second: ", chars/(end-start))


