import json

from bson import ObjectId
from json import loads, dumps


# Custom Mongo -> JSON encoder since none of the included ones work
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)


def doc_to_json(documents):
    return loads(dumps(documents, cls=MongoJSONEncoder))


def docs_to_json(documents):
    return loads(dumps(list(documents), cls=MongoJSONEncoder))
