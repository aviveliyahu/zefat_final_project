from flask import Flask, render_template, request, json, jsonify
import os
import openai
from openai import OpenAI

messages = [{'role': 'system', 
             'content': """
                Make sure the answers are not over 500 tokens.you are a occupational therapy assistant that talks with an intern therapist and try to help him solve problems in a socratic method.
                you answer in this field only,in case you are questioned about anything else you always reply that youre not familiar with this subject'
                """
             }]

client = OpenAI(
    # This is the default and can be omitted
    api_key="sk-proj-8riOJxXgXMf0P7uBTRZfT3BlbkFJrLMnTmNfMel1RqNN0z3Y",
)


app = Flask(__name__)

@app.route("/")
def home():
    return login()

@app.route("/main")
def ind():
    user_ip = request.remote_addr
    return render_template('index.html',user_ip = user_ip)

@app.route("/login")
def login():
    user_ip = request.remote_addr
    return render_template('login.html',user_ip = user_ip)

@app.route("/get", methods=["GET", "POST"])
def chat():
    data = request.get_json()
    msg = data.get("msg")

    if msg == "Save chat.":
        return save_chat()
    else:
        input = msg
        if(input == "Save chat."):
            return save_chat()
        else:
            messages.append({'role': 'user', 'content': input})
            return get_Chat_response(messages)
    
def save_chat():
    answer = "Chat saved!"
    json_string = json.dumps(messages)
    num = int(lastFileNum()) +1
    with open(f'data/json_data{num}.json', 'w') as outfile:
         outfile.write(json_string)
    return jsonify({"response": answer})


def lastFileNum():
    path = "data/"
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # Sort the files
    files.sort()
    # Get the last file
    if files:
        last_file = files[-1]
        # Return the last character of the last file
        return last_file[-6] if last_file else 0
    else:
        return 0
    
def get_Chat_response(text):
    chat = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=text,
    max_tokens=500,
    )
    reply = chat.choices[0].message.content
    messages.append({'role':'system','content':reply})
    return jsonify({"response": reply})


if __name__ == '__main__':
    app.run()