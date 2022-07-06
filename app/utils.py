from geojson import Point
from flask import jsonify

def error_to_output(error:RuntimeError):
    """
    Provides consistent formatting for error responses.

    Returns (dict) a dictionary containing the single key "error", with the error message.
    """
    return {
        "error": str(error)
    }

def get_point(coords: list) -> Point:
    """
    Accepts a set of coordinates and returns a GeoJson point

    Parameters:
    - coords (list): A list of float values representing a GeoJson point.  Should be 2 or 3 values.
    Returns geojson.Point 
    Throws: RuntimeError, when invalid coordinates are passed.

    Ref: https://pypi.org/project/geojson/#validation
    """
    obj = Point(coords)
    if not obj.is_valid:
        raise RuntimeError(f"Could not construct a GeoJson point from the coordinates {coords!r}: {obj.errors()!r}")
    return obj

class InvalidUsage(Exception):
    """
    Borrowed from https://flask.palletsprojects.com/en/0.12.x/patterns/apierrors/, 
    provides a consistent validation exception.
    """
    status_code = 400

    def __init__(self, error, status_code=None, payload=None):
        Exception.__init__(self)
        self.error = error
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        return rv


def to_float(value:int or str or float):
    """
    Converts a given value to float.
    Parameters: 
    value: Int or string or float value.
    Returns: Float value.
    Raises Exception if not one of the above types, or if string is not numeric in nature.
    """
    if isinstance(value, float):
        return value
    if isinstance(value, int):
        return float(value)
    if isinstance(value, str):
        if value.isnumeric():
            return float(value)
    raise RuntimeError(f"The passed value {value!r} is not a numeric string, float, or int value")
