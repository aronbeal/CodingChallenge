from flask import (
    Flask, 
    request, 
    make_response, 
    render_template, 
    jsonify
)
import os
from .points import get_all_points, get_points_in_radius, get_points_in_polygon
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from .db import connect
import psycopg2
from .utils import error_to_output, InvalidUsage
app = Flask(__name__)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/", methods=["GET"])
def home():
    """
    Renders a page showing all routes, making it easier to do things like submit POST values.
    """
    return render_template('home.html')

@app.route("/debug", methods=["GET"])
def debug():
    """
    Displays debugging information about the local environment.
    TODO: Restrict to local usage only.
    Returns (dict): containing keys:
    - env_vars: All defined container env vars.
    - tables: All defined db table names from the db.
    """
    cur = connect().cursor()
    try:
        cur.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'""")
        tables = []
        for record in cur.fetchall():     # or cur2.fetchone, fetchmany...
            tables.append(record[0])
        return {
            "env_vars": dict(os.environ),
            "tables": tables
        }
    except psycopg2.Error as e:
        return error_to_output(e)

@app.route("/points", methods=["GET", "POST"])
def points():
    """
    Displays a list of all points currently in the database, or adds one or more points to the db.
    TODO: This should optimally include paging before anything, as it 
    is a potential performance issue to retrieve all points in a db
    other than the test version.
    
    GET accepts query parameters:
    - r: Displays points within a given radius.
    - u: Units for distance when requesting a radius or polygon bounded output.
         Must be either 'f' (feet) or 'm' (meters).
    - c: center point when requesting a radius bounded output.  Values must be comma-separated.
         Example: 1,1
    - p: A series of points when requesting within a geographical polygon.   Values must be 
         comma-separated.  Example (rectangle): &p=[1,1],[1,5],[1,3],[3,5]
    Returns (dict): A dictionary object with the response, formatted as json output.
    Keys:
        - points: a list of point tuples representing the existing points in the system.
    
    POST accepts form parameter 'points', which should be a JSON list containing tuples of 
    points to add, e.g '{"points":[[1,1],[1,5],[1,3],[3,5]]}
    """
    error = None
    if request.method == 'POST':
        if request.form['points'] is None:
            raise RuntimeError(f"Missing key 'points' in request")
    if request.method == 'GET':
        if any(item in ['r', 'u', 'c'] for item in list(request.args.keys())):
            # Caller is requesting within a certain radius.
            if not 'r' in request.args.keys():
                raise InvalidUsage("The 'r' parameter is required when searching by radius")
            if not 'c' in request.args.keys():
                raise InvalidUsage("The 'r' parameter must always be accompanied by the 'c' parameter")
            if not 'u' in request.args.keys():
                raise InvalidUsage("The 'r' parameter must always be accompanied by the 'u' parameter")
            radius = request.args.get('r')
            center = request.args.get('c')
            units = request.args.get('u')
            
            return get_points_in_radius(radius=radius, center=center, units=units)
        if 'p' in request.args.keys():
            # Caller is requesting within a polygon
            return get_points_in_polygon(request.args.p)

        return get_all_points(request.args.get('l'))
    raise InvalidUsage(f"Unsupported method: {request.method!r}", status_code=405)


