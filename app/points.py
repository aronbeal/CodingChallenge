##
# File
# Various methods to retrieve points from the db based on parameters.
##
import psycopg2.extras
import pprint
import geojson
from .db import connect
from .utils import get_point, error_to_output, InvalidUsage, to_float


def add_points(coords: list) -> int:
    """ 
    For adding points to the database.
    Parameters:
    coords: A list of float tuples representing point coordinates.
    Returns (int) The number of records inserted.
    """
    for coordinates in coords:
        p = get_point(coordinates)

def get_all_points(limit:int=10) -> list:
    """
    Returns all points in the system.
    TODO: This should really have paging, for performance reasons.

    Returns (list): A list of tuples, each representing a
    """
    cur = connect().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute(
            f"""SELECT srid, auth_name, auth_srid, srtext, proj4text FROM public.spatial_ref_sys LIMIT {limit!r}""")
        points = []
        for record in cur.fetchall():     # or cur2.fetchone, fetchmany...
            points.append(record['srtext'])
        return {
            "srtext": points
        }
    except psycopg2.Error as e:
        return error_to_output(str(e))


def get_points_in_radius(radius: float, center: list, units: str) -> list:
    """
    Returns the points within a given radius.

    Parameters:
    - radius (float): The radius within which to return results for.  Inclusive.
    - center (tuple): a float tuple represent the center point to search from.
    - units (string): The string 'f' or 'm', meaning that the value of 'r' is in 
      feet or meters, respectively.
    """
    try:
        radius = to_float(radius)
    except RuntimeError as e:
        raise InvalidUsage("The 'r' parameter is required to be a float value")
    if units not in ['f', 'm']:
        raise InvalidUsage("Disallowed value for 'u' parameter (expected 'f' or 'm')")
    if not isinstance(center, list):
        raise InvalidUsage("The 'c' parameter must be a list of float values")
    # Convert center to point value.
    center = get_point(center)
    cur = connect().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("""
            SELECT srid, auth_name, auth_srid, srtext, proj4text 
            FROM public.spatial_ref_sys
        """)
        points = []
        for record in cur.fetchall():     # or cur2.fetchone, fetchmany...
            points.append(record['srtext'])
        return {
            "srtext": points
        }
    except psycopg2.Error as e:
        return error_to_output(str(e))


def get_points_in_polygon(coords: list):
    """
    Returns the points within a given polygon.  Not implemented, due to time constraints.

    Parameters:
    - coords (float): A list of tuples, each representing a point in the polygon.
    """
    raise RuntimeError("Not implemented, due to time constraints")
