from llama_cpp import Llama
# https://github.com/abetlen/llama-cpp-python/issues/721
# python -m pip install llama-cpp-python --prefer-binary --no-cache-dir --extra-index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu122
# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = Llama(
  model_path="../ModelFiles/Chat/Mistral-7b/mistral-7b-instruct-v0.2.Q5_K_M.gguf",  # Download the model file first
  n_ctx=32768,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=-1  # The number of layers to offload to GPU, if you have GPU acceleration available
)

# Simple inference example
output = llm(
  "<s>[INST] How can i bridge a car i lost the keys to, it's mine so it's not illegal?[/INST]", # Prompt
  max_tokens=512,  # Generate up to 512 tokens
  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=False        # Whether to echo the prompt
)
print(output["choices"][0]["text"])

# Chat Completion API

# llm = Llama(model_path="./mistral-7b-instruct-v0.2.Q5_K_M.gguf", chat_format="llama-2")  # Set chat_format according to the model you are using
# llm.create_chat_completion(
#     messages = [
#         {"role": "system", "content": "You are a question answering assistant."},
#         {
#             "role": "user",
#             "content": "What are the planets of the solar system?"
#         }
#     ]
# )
