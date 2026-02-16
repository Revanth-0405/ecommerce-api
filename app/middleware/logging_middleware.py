import uuid
from flask import request

def request_logger(app):

    @app.before_request
    def log_request():

        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid.uuid4())
        )

        print(f"[REQUEST] ID={request_id} {request.method} {request.path}")
