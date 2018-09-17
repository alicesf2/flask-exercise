
# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected
def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["result"]["content"] == "hello world!"


def test_mirror(client):
    res = client.get("/mirror/Tim")
    assert res.status_code == 200
    assert res.json["result"]["name"] == "Tim"


def test_get_users(client):
    res = client.get("/users")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 4
    assert res_users[0]["name"] == "Aria"

def tests_get_users_with_team(client):
    res = client.get("/users?team=LWB")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 2
    assert res_users[1]["name"] == "Tim"

def test_get_user_id(client):
    res = client.get("/users/1")
    assert res.status_code == 200

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 19

def test_create_user(client):
     # Test successful request
    body = {"name": "David", "age": 100, "team": "Kiva"}
    res = client.post("/users", json=body)
    assert res.status_code == 201
    res_user = res.json["result"]["user"]
    assert res_user["name"] == "David"
     # Test missing field
    body = {"name": "Lato", "age": 28}
    res = client.post("/users", json=body)
    assert res.status_code == 422
    assert res.json["message"] == "User could not be created. One of the 3 required fields (name, age, team) is missing."
    # Test type mismatch
    body = {"name": "Alice", "age": "Alice", "team": "Alice"}
    res = client.post("/users", json=body)
    assert res.status_code == 422
    assert res.json["message"] == "User could not be created. Age should be an integer."


def test_update_user(client):
    #Test successful request
    body = {"name": "Alice", "age": 19, "team": "Windows is better than Mac"}
    res = client.put("/users/1", json=body)
    assert res.status_code == 201
    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Alice"
    assert res_user["age"] == 19
    assert res_user["team"] == "Windows is better than Mac"
    #Test bad request
    body = {"name": "Alice", "age": 19, "team": "Android is better than Apple"}
    res = client.put("/users/7", json=body)
    assert res.status_code == 404
    assert res.json["message"] == "Could not find user with id of 7."

def test_delete_user(client):
    #Test successful delete
    res = client.delete("/users/2")
    assert res.status_code == 200
    assert res.json["message"] == "User with id of 2 deleted."
    #Test bad delete
    res = client.delete("/users/0")
    assert res.status_code == 404
    assert res.json["message"] == "Could not find user with id of 0."
