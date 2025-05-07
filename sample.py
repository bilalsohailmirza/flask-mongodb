from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

# flask flask-cors pymongo dnspython

app = Flask(__name__)
CORS(app)


MONGO_URI = "mongodb+srv://bsohail420:uzmRlJUJdvZFlDsK@myshelfdb.mdhjvni.mongodb.net/?retryWrites=true&w=majority&appName=myShelfDB"

client = MongoClient(MONGO_URI)

db = client["iot-database"]
reading_collection = db["readings"]


def serialize_object_id(document):
    if "_id" in document:
        document["_id"] = str(document["_id"])
    if "device_id" in document:
        document["device_id"] = str(document["device_id"])
    if "temprature" in document:
        document["temprature"] = str(document["temprature"])
    if "humidity" in document:
        document["humidity"] = str(document["humidity"])
    if "time" in document:
        document["time"] = str(document["time"])
    if "pressure" in document:
        document["pressure"] = str(document["pressure"])
    return document

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome you are accessing the REST API!"

### Routes for Authors
@app.route('/readings', methods=['GET'])
def get_authors():
    readings = list(reading_collection.find())
    return jsonify([serialize_object_id(reading) for reading in readings]), 200

@app.route('/readings', methods=['POST'])
def create_author():
    data = request.json
    # if not data.get("name"):
    #     return jsonify({"error": "Author name is required"}), 400
    reading_id = reading_collection.insert_one({"device_id": data["device_id"],
                                                "temprature": data["temprature"],
                                                "humidity": data["humidity"],
                                                "time": data["time"],
                                                "pressure": data["pressure"],
                                                }).inserted_id
    return jsonify({"message": "Reading created", "id": str(reading_id)}), 201


if __name__ == '__main__':
    app.run(debug=True)
