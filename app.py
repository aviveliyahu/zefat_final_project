from flask import Flask, render_template, request, json, jsonify
from datetime import datetime
from llm.rag import *
from llm.response import *
from users.users import *

llm_model = "1"

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
    data = request.get_json()
    user_id = data.get("user_id")
    choice = data.get("msg")

    check_db = search_user(str(user_id))

    if check_db == "yes":
        if choice=="1":
             return jsonify({"response": "/main"})
        elif choice=="2":
            llm_model = "2"
            return jsonify({"response": "/main"})
    else:
         return jsonify({"response": "0"})
    
@app.route("/get", methods=["GET", "POST"])
def chat():
    data = request.get_json()
    msg = data.get("msg")

    if msg == "Save chat.":
        return save_chat()
    else:
            input = msg
        # if(input == "Save chat."):
        #     return save_chat()
        # else:
            context = context_retrieve(input)
            append_message(f"{input}, external data:{context}",role="user")
            return get_Chat_response(messages,llm_model)

def save_chat():
    answer = "Chat saved!"
    json_string = json.dumps(messages,indent=4)
    current_date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    with open(f'data/{current_date_time}.json', 'w') as outfile:
         outfile.write(json_string)
    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run()