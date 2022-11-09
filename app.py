from flask import Flask, request,jsonify,Response
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

# database connection
try:
    mongo = pymongo.MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS=1000)
    db = mongo.crud
    mongo.server_info()#trigger exception if cannot connect to db

except:
    print("Error - cannot connect to db ")

#-------------------------------read user--------------------------------------------

@app.route("/users",methods=["GET"])
def read_user():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(data),
            status=500,
        )

    except Exception as ex:
        print(ex)
        return Response(
        response=json.dumps({"msg": "cannot read users"}),
        status=500,
        )

#-----------------------create user------------------------------------------------------
@app.route('/users',methods=["POST"])
def create_user():
    try:
        user = {"fname": request.form["fname"],
                "lname": request.form["lname"]
                }
        dbResponse = db.users.insert_one(user)
        #for attr in dir(dbResponse):
        #    print(attr)
        return Response(
            response=json.dumps({"msg":"user created"}),
            status=200,
        )
    except Exception as ex:
        print(ex)

#-------------------------------update user-----------------------------
@app.route("/users/<id>",methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"fname":request.form["fname"]}}
        )
        #for attr in dir(dbResponse):
        #   print(f"{attr}")
        if dbResponse.modified_count==1:

            return Response(
                response=json.dumps({"msg": "user updated"}),
                status=200,
            )

        return Response(
            response=json.dumps({"msg": "nothing to update"}),
            status=200,
            )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"msg": "user cannot updated"}),
            status=500,
        )
# ---------------delete user-----------------------
@app.route("/users/<id>",methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
            response=json.dumps({"msg": "user deleted","id":f"{id}"}),
            status=200,
            )
        return Response(
            response=json.dumps({"msg": "user not found ", "id": f"{id}"}),
            status=200,
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"msg": "user cannot delete"}),
            status=500,
        )





if __name__=='__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)