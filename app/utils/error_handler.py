from flask import jsonify

def error_response(message, code, status):
    return jsonify({
        "error": message,
        "code": code
    }), status
