from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

username = os.getenv('MONGODB_USER')
password = os.getenv('MONGODB_PASS')

def insert_user(user_id: str, name: str, role: str, field: str):
    uri = f"mongodb+srv://{username}:{password}@cluster0.5sfu0s0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)

    # database and collection code goes here
    db = client.zefat_project
    collection = db.users

    result = search_user(user_id)
    
    if result[0] == "no":
        docs = {"name": name, "id_number": user_id, "role": role, "field": field}
        collection.insert_one(docs)
        client.close()
        return "OK"
    else:
        client.close()
        return "NO"


# find if user in DB
def search_user(user_id: str):
    uri = f"mongodb+srv://{username}:{password}@cluster0.5sfu0s0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)

    # database and collection code goes here
    db = client.zefat_project
    collection = db.users

    cursor = collection.find({"id_number": user_id})
    result = list(cursor)

    if not result:
        return ["no"]
    else:
        user = result[0]
        return ["yes",
                user.get("name", ""),
                user.get("id_number", ""),
                user.get("role", ""),
                user.get("field", "")
                ]
def insert_error(user_id: str, name: str, role: str, field: str,error,text):
    uri = f"mongodb+srv://{username}:{password}@cluster0.5sfu0s0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)

    # database and collection code goes here
    db = client.zefat_project
    collection = db.errors
    current_date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    docs = {"time":current_date_time,"name": name, "id_number": user_id, "role": role, "field": field,"error":error,"input":text}
    collection.insert_one(docs)
    client.close()