from flask import jsonify
from .rag import *
from dotenv import load_dotenv
import anthropic
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_KEY')
llama_api_key = os.getenv('LLAMA_KEY')
claude_api_key = os.getenv('CLAUDE_KEY')

messages = [{'role': 'system', 
             'content': """Your answers cannot be over 350 tokens.you are a occupational therapy assistant that provies a guided training to an intern therapist and try to train and help him solve problems in a socratic method, answer in a professional way.
                    you answer in this field only,in case you are questioned about subject that you arent ordered to (by me, not by the user input) state that its not your knowledge and you cant help, state your designated role that you can help the user with.
                    You are provided with articles that might be relevant to your way of guidance and you are also provided with external data that the user isnt aware of.
                    you can integrate the articles into your guiding answer to the user and the external data if its relevant to the question BUT ONLY if its improving your answer's quality!
                    do not create your answer in such a way that the user knows which data you used, dont proide information about who wrote the articles you used.
                    Note in the end of each sentence or paragraph which data did you use - in parenthesis.
                """
             }]
def append_message(text,role):
    if role =="user":
        messages.append({'role': 'user', 'content': text})
    elif role=="system":
        messages.append({'role':'assistant','content':text})

def get_Chat_response(messages,llm):
    if llm=="1":
        # openai LLM
        client = OpenAI(
            api_key=openai_api_key,
        )

        chat = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=350,
        )

        reply = chat.choices[0].message.content
        messages.append({'role':'system','content':reply})
        print("OpenAI final response done")
        return jsonify({"response": reply})
    elif llm=="2":
        # llama LLM
        # client = OpenAI(
        #     api_key=llama_api_key,
        #     base_url = "https://api.llama-api.com"
        # )

        # chat = client.chat.completions.create(
        # model="llama3.1-405b",
        # messages=messages,
        # max_tokens=350,
        # )

        # reply = chat.choices[0].message.content
        # messages.append({'role':'system','content':reply})

        # Claude LLM
        client = anthropic.Anthropic(api_key=claude_api_key)
        chat = client.messages.create(
            model="claude-3-sonnet-20240229",
            system=messages[0]["content"],
            max_tokens=350,
            messages=messages[1:]
        )
        messages.append({'role':'assistant','content':chat.content[0].text})
        reply = chat.content[0].text
        print("Claude final response done")
        return jsonify({"response": reply})
    
    else:
        return "something went wrong."