import threading
import uuid
import time

from ResponseHandler.InferenceHandler import InferenceHandler


class Handler:
    def __init__(self, memory_handler: InferenceHandler):
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
                    print("Solving request with config: ", request["model_config"])
                    output = self.memory_handler.inference(model_config=request["model_config"])
                    print("Solved request " + str(request["request_uuid"]))
                    return output
            time.sleep(0.5)

    def update_queue(self):
        reordered_queue = []
        priority_1_requests = [[], []]
        priority_2_requests = []
        for e in self.queue:
            if e["priority"] == 0:
                reordered_queue.append(e)
            if e["priority"] == 1:
                if e["model_config"]["model_name"] == self.memory_handler.current_model_name:
                    priority_1_requests[0].append(e)
                else:
                    priority_1_requests[1].append(e)
            if e["priority"] == 2:
                priority_2_requests.append(e)
        reordered_queue.extend(priority_1_requests[0])
        reordered_queue.extend(priority_1_requests[1])
        reordered_queue.extend(priority_2_requests)

        self.queue = reordered_queue
