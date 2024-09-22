from flask import Flask, render_template, request, json, jsonify
from datetime import datetime
from llm.rag import *
from llm.response import *
from users.users import *
import asyncio

llm_model = "1"
role = ""
field = ""
check_db = []
name = ""
name_check = False

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
    global check_db 
    global name
    
    data = request.get_json()
    user_id = data.get("user_id")
    choice = data.get("msg")

    check_db = search_user(str(user_id))

    if check_db[0] == "yes":
        role = check_db[3]
        field = check_db[4]
        name = check_db[1]

        if choice=="1":
             return jsonify({"response": "/main"})
        elif choice=="2":
            llm_model = "2"
            return jsonify({"response": "/main"})
    else:
         return jsonify({"response": "0"})
    

@app.route("/get", methods=["GET", "POST"])
async def chat():
    data = request.get_json()
    msg = data.get("msg")

    if msg == "Save chat.":
        return save_chat()
    else:
        try:
            input = msg
            if field == "Therapy":
                if name_check == False:
                    append_message(f"user's name: {name}",role="user",field=field)
                    name_check = True
                context_task = asyncio.to_thread(context_retrieve, input, "cases")
                guidance_task = asyncio.to_thread(guidance_generation, input, llm_model)

                context, guidance = await asyncio.gather(context_task, guidance_task)

                articles = await asyncio.to_thread(context_retrieve, guidance, "articles")

                await asyncio.to_thread(append_message, f"{input}, articles = {articles}, external data:{context}", role="user",field= field)
                response = await asyncio.to_thread(get_Chat_response, therapy_messages, llm_model)
                return response
            elif field == "Food":
                if name_check == False:
                    append_message(f"user's name: {name}",role="user",field=field)
                    name_check = True
                context_task = asyncio.to_thread(context_retrieve, input, "recipes")
                context = await context_task

                await asyncio.to_thread(append_message, f"{input}, external recipes:{context}", role="user",field= field)
                
                response = await asyncio.to_thread(get_Chat_response, food_messages, llm_model)
                return response
        except Exception as e:
                    reply = "Unexpected error, contact system admin."
                    print("Error occurred.")
                    try:
                        print("start insert error")
                        insert_error(user_id=check_db[2],name=check_db[1],role=check_db[3],field=check_db[4],error=str(e),text=input)
                        print("done insert error")
                    except:
                        return jsonify({"response": reply})
                    return jsonify({"response":reply})


def save_chat():
    answer = "Chat saved!"
    if field == "Food":        
        json_string = json.dumps(food_messages,indent=4)
        current_date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        with open(f'data/{current_date_time}.json', 'w') as outfile:
            outfile.write(json_string)
        return jsonify({"response": answer})
    elif field == "Therapy":
        json_string = json.dumps(therapy_messages,indent=4)
        current_date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        with open(f'data/{current_date_time}.json', 'w') as outfile:
            outfile.write(json_string)
        return jsonify({"response": answer})


@app.route("/user",methods=["GET", "POST"])
def user():
    if role != "" and field!="": 
        return [role,field,name]
    else:
        return ["no"]
    
@app.route("/add",methods=["POST"]) 
def add():
    name = request.form.get("name")   
    id_number = request.form.get("id_number")
    user_role = request.form.get("role")
    print(f"Added user: name - {name}, id_number - {id_number}, user_role - {user_role}, field - {field}")
    status = insert_user(id_number,name,user_role,field)
    return status

if __name__ == '__main__':
    app.run()