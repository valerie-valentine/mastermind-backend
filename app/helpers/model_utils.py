from flask import abort, make_response
from ..db import db


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)

    except KeyError as error:
        response = {"details": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return {f"{cls.__name__}".lower(): new_model.to_dict()}, 201
