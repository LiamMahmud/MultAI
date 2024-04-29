from flask import Response


def bad_request(error):
    print('Error: ' + error)
    return Response(
        error,
        status=400,
    )


def internal_server_error(error):
    print('Error: ' + error)
    return Response(
        error,
        status=500,
    )
