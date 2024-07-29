import pymongo

url = "mongodb://localhost:27017/"
client = pymongo.MongoClient(url)
db = client["user_crud"]

user_collection = db.get_collection("user_info")
id_collection = db.get_collection("id_collection")
