from flask import Flask
from flask import request
from data_handler import DataHandler

app = Flask(__name__)
data_handler = DataHandler()



@app.route("/", methods=["POST"])
def hello_world():
    return "<p>DroneMR server</p>"
    


@app.route("/init", methods=["GET", "POST"])
def init():
    data = request.json
    print(data)
    response = data_handler.process_data(data)
    return response


@app.route("/drones", methods=["GET"])
def drones():
    if data_handler.leader_drone == None :
        return {
            "leader": data_handler.leader_drone,
            "slaves" : list(data_handler.slave_drones.keys())
        }
    else :
        return {
            "leader": data_handler.leader_drone.name,
		    "slaves": list(data_handler.slave_drones.keys()),
        }


@app.route("/position/<drone_name>", methods=["POST"])
def position(drone_name):
    if (drone_name not in data_handler.slave_drones) and (
        drone_name != data_handler.leader_drone.name
        
    ):
        print("problem", drone_name, data_handler.slave_drones, drone_name not in data_handler.slave_drones)
        return {"success": False, "message": "drone not initialized"}
    else:
        print("no problem")
        data = request.json
        response = data_handler.process_data(data)
        return response


@app.route("/detection", methods=["GET", "POST"])
def detection():
    data = request.json
    response = data_handler.process_data(data)
    return response


@app.route("/headingCommand/<drone_name>", methods=["GET"])
def headingCommand(drone_name) :
    return data_handler.heading_directive_json(drone_name)

@app.route("/moveCommand/<drone_name>", methods=["GET"])
def moveCommand(drone_name) :
    return data_handler.get_move_directive(drone_name)

@app.route("/test", methods=["GET", "POST"])
def test():
    return str(request.json)

    # if request.method == "POST":
    #     print(request)
    #     return "<p>" + request.form["username"] + "</p>"
    # else:
    #     return "<p>got</p>"


# from flask import Flask
# from flask_restful import Api, Resource

# app = Flask(__name__)
# api = Api(app)

# users = []
# id = 0


# class UserAPI(Resource):
#     def get(self, name):
#         for user in users:
#             if user["name"] == name:
#                 return user

#     def post(self, name):
#         global id
#         user = {"name": name, "id": id}
#         id += 1
#         users.append(user)
#         return user


# api.add_resource(UserAPI, "/users/<string:name>", endpoint="user")

if __name__ == "__main__":
            app.run(debug=False, host="0.0.0.0")
           