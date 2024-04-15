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

    def add_request(self, model_config, reqid=uuid.uuid4()):
        self.queue.append({"request_uuid": reqid, "model_config": model_config, "priority": model_config["priority"]})
        return {"request_uuid": reqid, "model_config": model_config, "priority": model_config["priority"]}

    def remove_request(self, request):
        self.queue.remove(request)

    def resolve_request(self, request):
        while True:
            if self.queue.index(request) == 0:
                with self.lock:
                    output = self.memory_handler.inference(model_config=request["model_config"])
                    print("Done")
                    return output
            time.sleep(0.5)

    def update_queue(self):
        reorder = []
        hold = [[], []]
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
