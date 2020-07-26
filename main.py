from flask import Flask, request, jsonify, make_response
import jwt
from werkzeug import exceptions
from datetime import datetime, timedelta
from efemerides import efemerides
from calendar import monthrange
from user_info import users
from functools import wraps
from flask_caching import Cache


cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)

# Avoid values reordering in JSON data
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = "secret"


def tokenRequired(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        # Get token from HTTP header if exists
        try:
            token = request.headers['x-access-token']
        except KeyError:
            return jsonify({"message": "Token is missing"}), 401
        
        try:
            print(token)
            user_data = jwt.decode(token, app.config['SECRET_KEY'])
            #print(user_data)
            current_user = [user for user in users if user["username"]==user_data['user']]
        except:
            return jsonify({"message": "Invalid token"}),401
        
        return function(current_user[0], *args, **kwargs)
    return decorated


@app.route("/login")
def login():
    """ This function is intended to get an authentication token to access 
    protected routes """

    auth = request.authorization 
    if auth is not None:
        username = auth.username
        password = auth.password

        # Check if user is registered and if the password is valid
        current_user = [user for user in users if user["username"]==username]
        if  len(current_user) > 0 and password == current_user[0].get("password"):
            # Creates token for requests
            token = jwt.encode({'user': username, 'exp':datetime.utcnow() + timedelta(minutes=5)}, app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('UTF-8')})

    # Notifies the browser that authentication is required
    return make_response("User not registered", 401, {"WWW-Authenticate": "Basic realm='Login Required'"})


@app.route("/efemerides", methods=['GET'])
@tokenRequired
def getEfemerides(current_user):
    # Get query string from URL
    queryDay = request.args.get('day')
    
    # Check format for input data. It must be: YYYY-MM-DD
    try:
        # FIXME: Python 3.6 bug: It doesn't return zero-padded months and days, 
        # as it should be
        date = datetime.strptime(queryDay, "%Y-%m-%d")    
    except ValueError:
        raise exceptions.BadRequest
    except TypeError:
         raise exceptions.BadRequest
    else:
        event = getEntry(date)
        return jsonify(event), 200


# NOTE: Eventually, this would be a database query
#@cache.cached(timeout=30, key_prefix='entry')
@cache.memoize(timeout=60)
def getEntry(date):
    # Format day and month as zero-padded string
    day = "{:02d}".format(date.day)
    month = "{:02d}".format(date.month)
    # Get number of days for a given year/month pair
    num_days = monthrange(date.year, date.month)[1]
    # Get events for all days in a month, even for those which don't have any registered events
    month_events = {
        "{:02}".format(i):efemerides.get(month).get("{:02}".format(i)) for i in range(1,num_days+1)
        }
    event = {day:efemerides.get(month).get(day), month:month_events}
    return event


@app.errorhandler(exceptions.BadRequest)
def handleInvalidQuery(error):
    return jsonify({"message":"Queries must be in format 'YYYY:MM:DD'\
        and must include valid dates"}),400


@app.errorhandler(exceptions.MethodNotAllowed)
def handleMethodNotAllowed(error):
    return jsonify({"message":"Only GET method is accepted"}),405


if __name__ == "__main__":
    app.run(debug=True, port=5000)