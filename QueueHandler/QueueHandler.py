import threading
import uuid
import time

from MemoryHandler.MemoryHandler import MemoryHandler
# TODO try to fix order of execution and change in mem handler append to substitute element0 si sneak == False
class Handler:
    def __init__(self, memory_handler: MemoryHandler, ):
        self.queue = []
        self.memory_handler = memory_handler
        self.lock = threading.Lock()

    def add_request(self, model_config):
        reqid = uuid.uuid4()
        self.queue.append({"request_uuid": reqid, "model_config": model_config, "priority": model_config["priority"]})
        return {"request_uuid": reqid, "model_config": model_config, "priority": model_config["priority"]}

    def remove_request(self, request):
        self.queue.remove(request)

    def check_turn(self, request):
        request_index = self.queue.index(request)
        if request_index == 0:
            return True
        return False

    def resolve_request(self, request):
        """
        Checks if it's the request's turn, request queue updates are done each time
        :param request:
        :return: inference output
        """
        while True:
            with self.lock:
                if self.check_turn(request):
                    output = self.memory_handler.inference(model_config=request["model_config"])
                    print("done 0")
                    self.remove_request(request)
                    return output

    def update_queue(self):
        reorder = []
        hold = [[],[]]
        last = []
        for e in self.queue:
            if e["priority"] == 0:
                reorder.append(e)
            if e["priority"] == 1:
                if e["model_config"]["model_name"] == self.memory_handler.current_model_name:
                    hold[0].append(e)
                else:
                    hold[1].append(e)
            if e["priority"] == 2:
                last.append(e)
        reorder.extend(hold[0])
        reorder.extend(hold[1])
        reorder.extend(last)
        self.queue = reorder


    # def can_sneak_in(self, request):
    #     request_index = self.queue.index(request)
    #     if self.queue == [request]:
    #         return True
    #
    #     for i in self.queue:
    #         if i["priority"] == 0:
    #             return False
    #
    #     for i in range(request_index):
    #         if self.queue[i]['priority'] == 1 and self.queue[i]["model_config"]['model_name'] == self.memory_handler.current_model_name:
    #             return False
    #
    #     return self.memory_handler.current_model_name == request["model_config"]["model_name"]
    #
    # def can_be_sneaked_over(self, request):
    #     request_index = self.queue.index(request)
    #
    #     if request["model_config"]['model_name'] == self.memory_handler.current_model_name and request["priority"] == 1:
    #         return False
    #
    #     for next_index in range(request_index + 1, len(self.queue)):
    #         next_request = request[next_index]
    #         if next_request['priority'] == 1 and next_request["model_config"]['model_name'] == self.memory_handler.current_model_name:
    #             return True
    #
    #     return False
    #
    # def max_priority_handler(self, request):
    #     request_index = self.queue.index(request)
    #
    #     for i in range(request_index):
    #         if self.queue[i]['priority'] == 0:
    #             return False
    #     return True


# prompt = [
#     {"role": "system", "content": "You are a question answering assistant."},
#     {"role": "user", "content": "Tell me a number from 1 to 100"},
#     {'role': 'assistant', 'content':  'Sure! The answer is... 42!'},
#     {"role": "user", "content": "Do you remember what number you said before?"}
# ]
# i = {"model_name": "Llama2-7b", "n_gpu_layers": -1, "n_threads": 14, "main_gpu": 0,
#          "prompt": prompt, "temperature": 0.1, "max_tokens": 512, "top_p": 0.95,
#          "top_k": 40, "stream": False, "presence_penalty": 0.0, "frequency_penalty": 0.0,
#          "repeat_penalty": 1.1, "stop": None, "priority": 1
#          }


# y = MemoryHandler()
# x = Handler(y)
# r = x.add_request(i)
# print(x.can_sneak_in(request=r))
