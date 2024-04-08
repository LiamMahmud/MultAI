from llama_cpp import Llama

llm = Llama(
    model_path="../ModelFiles/Llama2-7b/llama-2-7b-chat.Q5_K_M.gguf",  # Download the model file first
    n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
    n_threads=14,  # The number of CPU threads to use, tailor to your system and the resulting performance
    n_gpu_layers=-1) # The number of layers to offload to GPU, if you have GPU acceleration available

# import objsize
# print(objsize.get_deep_size(llm))
# Simple inference example
# output = llm(
#   "[INST] <<SYS>> {Que planetas hay en el sistema solar?} <</SYS>>", # Prompt
#   max_tokens=1048,  # Generate up to 512 tokens
#   stop=["[/INST]"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
#   echo=False      # Whether to echo the prompt
#   #stream=True
# )
#
# print(output['choices'][0]['text'])


# llm = Llama(model_path="./mistral-7b-instruct-v0.2.Q5_K_M.gguf", chat_format="llama-2")  # Set chat_format according to the model you are using
print(llm.create_chat_completion(
    messages = [
        {"role": "system", "content": "You are a question answering assistant."},
        {"role": "user", "content": "Tell me a number from 1 to 100"},
        {'role': 'assistant', 'content': '  Sure! The answer is... 42!'},
        {"role": "user", "content": "Do you remember what number you said before?"}
    ]
))



# print(llm.create_chat_completion(
#     messages = [
#         {"role": "system", "content": "You are a question answering assistant."},
#         {"role": "user", "content": "Tell me a number from 1 to 100"},
#         {'role': 'assistant', 'content': '  Sure! The answer is... 42!'},
#         {"role": "user", "content": "Tell me anotherone"}
#     ]
# ))

# ----------------------------------------------------------------------------------------------------------------------------
# result = ""
# stream_generator = llm.create_chat_completion(
#     messages = [
#         {"role": "system", "content": "You are a question answering assistant."},
#         {"role": "user", "content": "Tell me a number from 1 to 100"},
#         {'role': 'assistant', 'content': '  Sure! The answer is... 42!'},
#         {"role": "user", "content": "Do you remember what number you said before?"}
#     ],
#     stream=True,
# )
# for out in stream_generator:
#     if "content" in out['choices'][0]['delta']:
#         print(out['choices'][0]['delta']["content"], end='')

# start = time.time()
#
# chars = 0
# args = {
#     "prompt": "[INST] <<SYS>> {What are the planets on the solar system?} <</SYS>>", # Prompt
#     "max_tokens":1048,  # Generate up to 512 tokens
#     "stop":["[/INST]"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
#     "echo":False,
#     "stream":True  # Whether to echo the prompt
# }
#
# for chunk in llm(**args):
#     print(chunk["choices"][0]["text"], end="")
#     chars += len(chunk)
#
# end = time.time()
# print("Time taken: ", end-start)
# print("chars per second: ", chars/(end-start))
