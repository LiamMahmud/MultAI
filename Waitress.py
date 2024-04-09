from waitress import serve

from API import app
from MemoryHandler.MemoryHandler import MemoryHandler
from QueueHandler.QueueHandler import Handler

memory_handler = MemoryHandler()
queue_handler = Handler(memory_handler)
app.logger.addHandler(queue_handler)

serve(app, host='0.0.0.0', port=8080)
