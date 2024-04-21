from flask import abort, make_response
import requests
import os


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"details": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"details": f"{cls.__name__} {model_id} not found"}, 404))

    return model
