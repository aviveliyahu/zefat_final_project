from pymongo import MongoClient
from dotenv import load_dotenv
import os

username = os.getenv('MONGODB_USER')
password = os.getenv('MONGODB_PASS')

def insert_user(user_id:str,name:str,role:str):
    uri = f"mongodb+srv://{username}:{password}@cluster0.5sfu0s0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)

    # database and collection code goes here
    db = client.zefat_project
    collection = db.users

    result = search_user(user_id)
    if result=="no":
        docs = {"name": name, "id_number":user_id,"role":role}
        collection.insert_one(docs)
        print("Created new user.")
    else:
        print("User already registered.")

    client.close()


# find if user in DB
def search_user(user_id:str):
    uri = f"mongodb+srv://{username}:{password}@cluster0.5sfu0s0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)

    # database and collection code goes here
    db = client.zefat_project
    collection = db.users

    cursor = collection.find({"id_number": user_id})
    result = list(cursor)

    if not result:
        return "no"
    else:
        return "yes"