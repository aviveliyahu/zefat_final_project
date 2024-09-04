from flask import Flask, render_template, request, json, jsonify
from datetime import datetime
from llm.rag import *
from llm.response import *
from users.users import *
import asyncio

llm_model = "1"
role = ""
field = ""

app = Flask(__name__)

@app.route("/main")
def ind():
    user_ip = request.remote_addr
    return render_template('index.html',user_ip = user_ip)

@app.route("/")
def login():
    user_ip = request.remote_addr
    return render_template('login.html',user_ip = user_ip)

@app.route("/llm", methods=["GET", "POST"])
def llm_choice():
    global llm_model
    global role
    global field

    data = request.get_json()
    user_id = data.get("user_id")
    choice = data.get("msg")

    check_db = search_user(str(user_id))

    if check_db[0] == "yes":
        role = check_db[3]
        field = check_db[4]

        if choice=="1":
             return jsonify({"response": "/main"})
        elif choice=="2":
            llm_model = "2"
            return jsonify({"response": "/main"})
    else:
         return jsonify({"response": "0"})
    
    
@app.route("/user",methods=["GET", "POST"])
def user():
    if role != "" and field!="": 
        return [role,field]
    else:
        return ["no"]
    
@app.route("/add",methods=["POST"]) 
def add():
    name = request.form.get("name")   
    id_number = request.form.get("id_number")
    user_role = request.form.get("role")
    print(name)
    print(id_number)
    print(user_role)
    print(field)
    status = insert_user(id_number,name,user_role,field)
    return status


@app.route("/get", methods=["GET", "POST"])
async def chat():
    data = request.get_json()
    msg = data.get("msg")

    if msg == "Save chat.":
        return save_chat()
    else:
            input = msg
            context_task = asyncio.to_thread(context_retrieve, input, "cases")
            guidance_task = asyncio.to_thread(guidance_generation, input, llm_model)

            context, guidance = await asyncio.gather(context_task, guidance_task)

            articles = await asyncio.to_thread(context_retrieve, guidance, "articles")

            await asyncio.to_thread(append_message, f"{input}, articles = {articles}, external data:{context}", role="user")
            response = await asyncio.to_thread(get_Chat_response, messages, llm_model)
            return response

def save_chat():
    answer = "Chat saved!"
    json_string = json.dumps(messages,indent=4)
    current_date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    with open(f'data/{current_date_time}.json', 'w') as outfile:
         outfile.write(json_string)
    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run()