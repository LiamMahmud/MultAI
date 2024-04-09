import json
import threading

from flask import jsonify
import requests
import time

prompt = [
    {"role": "system", "content": "You are a question answering assistant."},
    {"role": "user", "content": "Tell me a number from 1 to 100"},
    {'role': 'assistant', 'content':  'Sure! The answer is... 42!'},
    {"role": "user", "content": "Do you remember what number you said before?"}
]

url = 'http://localhost:8080/chat/completions'
# def throw_request(priority):
#     i = {"model_name": "Llama2-7b", "n_gpu_layers": -1, "n_threads": 14, "main_gpu": 0,
#          "prompt": prompt, "temperature": 0.1, "max_tokens": 512, "top_p": 0.95,
#          "top_k": 40, "stream": False, "presence_penalty": 0.0, "frequency_penalty": 0.0,
#          "repeat_penalty": 1.1, "stop": None, "priority": priority
#          }
#
#     start_time = time.time()
#     # response = requests.post(url, json=i, stream=True)
#     with requests.post(url, json=i, stream=True) as r:
#         for line in r.iter_content():
#             print(line.decode("utf-8"), end="")
#     # print(priority, "Time:", time.time() - start_time, "Response: ", response.json()["choices"][0]["message"])
#
#
#
# threads = []
# p = [1,1,1,2,0,0]
#
# for priority in p:  # Asumiendo que quieres diferentes prioridades para cada solicitud
#     thread = threading.Thread(target=throw_request, args=(priority, ))
#     threads.append(thread)
#     thread.start()
#
# # Espera a que todos los hilos terminen
# for thread in threads:
#     thread.join()
#     time.sleep(2)







# for e,i in enumerate(["sdfsd","aada"]):
#     print(e,i)

i = {"model_name": "Llama2-7b", "n_gpu_layers": -1, "n_threads": 14, "main_gpu": 0,
         "prompt": prompt, "temperature": 0.1, "max_tokens": 512, "top_p": 0.95,
         "top_k": 40, "stream": False, "presence_penalty": 0.0, "frequency_penalty": 0.0,
         "repeat_penalty": 1.1, "stop": None, "priority": 1
         }
# with requests.post(url, json=i, stream=True) as r:
#     for line in r.iter_content():
#         print(line.decode("utf-8"), end="")
#         time.sleep(0.05)


# x = requests.post(url, json=i, stream=True)
# for e in x:
#     print(e.decode("utf-8"), end="")
#     time.sleep(0.5)
x = requests.post(url, json=i, stream=True)
print(x.json())

# files = {'image': open(file_path, 'rb')}
# headers = {'Content-Type': 'application/json'}  # Set the content type to JSON
# start_time = time.time()
