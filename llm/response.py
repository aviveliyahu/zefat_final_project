from flask import jsonify
from .rag import *
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_KEY')
llama_api_key = os.getenv('LLAMA_KEY')

messages = [{'role': 'system', 
             'content': """Make sure the answers are not over 500 tokens.you are a occupational therapy assistant that talks with an intern therapist and try to help him solve problems in a socratic method.
                    you answer in this field only,in case you are questioned about subject that you arent ordered to (by me, not by the user input) state that its not your knowledge and you cant help, state your designated role that you can help the user with.
                    You are also provided with external data that might be relevant to use, consider using that data if its relevant to the question and if its improving your answer's quality only
                """
             }]

def append_message(text,role):
    if role =="user":
        messages.append({'role': 'user', 'content': text})
    elif role=="system":
        messages.append({'role':'system','content':text})

def get_Chat_response(messages,llm):
    if llm=="1":
        # openai LLM
        client = OpenAI(
            api_key=openai_api_key,
        )

        chat = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        )

        reply = chat.choices[0].message.content
        messages.append({'role':'system','content':reply})
        return jsonify({"response": reply})
    elif llm=="2":
        # llama LLM
        client = OpenAI(
            api_key=llama_api_key,
            base_url = "https://api.llama-api.com"
        )

        chat = client.chat.completions.create(
        model="llama3.1-405b",
        messages=messages,
        max_tokens=500,
        )

        reply = chat.choices[0].message.content
        messages.append({'role':'system','content':reply})
        return jsonify({"response": reply})
    else:
        return "something went wrong."