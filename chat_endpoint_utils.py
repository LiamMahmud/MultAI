import time


def stream_output(queue_handler, generator, req):
    try:
        for token in generator:
            if "content" in token['choices'][0]['delta']:
                content = token['choices'][0]['delta']["content"]
                yield content
        queue_handler.remove_request(req)
    except GeneratorExit:
        print("Upsss!")


def allowed_audio_file(filename):
    ALLOWED_EXTENSIONS = {"flac", "mp3", "mp4", "mpeg", "mpga", "m4a", "ogg", "wav", "webm"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
