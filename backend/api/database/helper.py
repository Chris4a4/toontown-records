import json

from typing import Any
from bson import ObjectId


# Custom Mongo -> JSON encoder since none of the included ones work
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)