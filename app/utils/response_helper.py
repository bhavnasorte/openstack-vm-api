from flask import jsonify

def success(data, status_code=200):
    return jsonify({"data": data, "error": None}), status_code

def error(message, status_code=400):
    return jsonify({"data": None, "error": message}), status_code
