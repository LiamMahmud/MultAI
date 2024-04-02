from multiprocessing.dummy import Pool

import requests

pool = Pool(20) # Creates a pool with ten threads; more threads = more concurrency.
                # "pool" is a module attribute; you can be sure there will only
                # be one of them in your application
                # as modules are cached after initialization.

if __name__ == '__main__':
    futures = []
    prompt = [
        {"role": "system", "content": "You are a question answering assistant."},
        {"role": "user", "content": "Tell me a number from 1 to 100"},
        {'role': 'assistant', 'content': 'Sure! The answer is... 42!'},
        {"role": "user", "content": "Do you remember what number you said before?"}
    ]

    i = {"model_name": "Mistral-7b", "n_gpu_layers": -1, "n_threads": 14, "main_gpu": 0,
         "prompt": prompt, "temperature": 0.1, "max_tokens": 512, "top_p": 0.95,
         "top_k": 40, "stream": False, "presence_penalty": 0.0, "frequency_penalty": 0.0,
         "repeat_penalty": 1.1, "stop": None
         }

    # Make a POST request to the API endpoint
    url = 'http://localhost:5000/chat'
    for x in range(20):
        futures.append(pool.apply_async(requests.post, (url,), {'json': i}))
    # futures is now a list of 10 futures.
    for future in futures:
        print(future.get().json()) # For each future, wait until the request finished and then print the response object.
