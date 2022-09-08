import pymongo, hashlib
from server import conf

myclient = pymongo.MongoClient(conf("mongodb"))
mydb = myclient["users"]
mycol = mydb["users"]

def create_user(username, password):
    user = {"username": username, "password": hashlib.sha256(password.encode('utf-8')).hexdigest()}
    for x in mycol.find({"username": username}):
        if x["username"] == username:
            return False
        else:
            mycol.insert_one(user)
            return True

def check_user(username, password):
    user = mycol.find_one({"username": username})
    if user:
        if user['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
            return True
        else:
            return False
    else:
        return False
