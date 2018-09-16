from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


@app.route("/users", methods=["GET", "POST"])
def get_users():
    if (request.method == "GET"):
        #if no team request received, return all users
        if (request.args.get("team") == None):
            data = {"users": db.get("users")}
            success_message = "Retrived all users."
            return create_response(data = data, message = success_message)
        else:
            #if team request received, check if team exists first
            team = request.args.get("team")
            if (len(db.getByTeam("users", team)) != 0):
                data = {"users": db.getByTeam("users", team)}
                success_message = "Retrieved all users on team " + team + "."
                return create_response(data = data, message = success_message)
            else:
                #if team does not exist, return error msg
                error_message = "The team " + team + " does not exist."
                return create_response(status = 404, message = error_message)

    if (request.method == "POST"):
        #get new user info in json form
        payload = request.get_json()
        error_message = "User could not be created."

        if (type(payload["name"]) != str):
            error_message += " Name should be a string."
            return create_response(status = 422, message = error_message)
        if (type(payload["age"]) != int):
            error_message += " Age should be an integer."
            return create_response(status = 422, message = error_message)
        if (type(payload["team"]) != str):
            error_message += " Team should be a string."
            return create_response(status = 422, message = error_message)
        else:
            data = {"new_user": db.create("users", payload)}
            success_message = "New user created!"
            return create_response(data = data, status = 201, message = success_message)


@app.route("/users/<id>", methods=["GET", "PUT", "DELETE"])
def get_user_by_id(id):
    id = int(id)
    if (request.method == "GET"):
        if (db.getById("users", id) != None):
            data = {"users": db.getById("users", id)}
            success_message = "Retrieved user with id of " + str(id) + "!"
            return create_response(data = data, message = success_message)
        else:
        #if user doesn't exist, return 404 with error message
            data = {"users": db.getById("users", id)}
            error_message = "Could not find user with an id of " + str(id) + "."
            return create_response(data = data, status = 404, message = error_message)

    if (request.method == "PUT"):
        if (db.getById("users", id) != None):
            update_values = request.get_json()
            data = {"users": db.updateById("users", id, update_values)}
            success_message = "User info updated."
            return create_response(data = data, status = 201, message = success_message)
        else:
            error_message = "Could not find user with id of " + str(id) + "." 
            return create_response(status = 404, message = error_message)

    # if (request.method == "DELETE"):

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
