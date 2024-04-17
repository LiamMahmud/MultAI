from flask import jsonify


def bad_request(error):
    print(error)
    return jsonify({'error:': error, "code:": 400})


def internal_server_error(error):
    return jsonify({'error:': error, "code:": 500})
