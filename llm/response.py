from flask import jsonify
from .rag import *
from dotenv import load_dotenv
import anthropic
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_KEY')
llama_api_key = os.getenv('LLAMA_KEY')
claude_api_key = os.getenv('CLAUDE_KEY')

therapy_messages = [{'role': 'system', 
                'content': f"""Your answers cannot be over 600 tokens so take that in account in your answers length.you are a occupational therapy assistant that provides a guided training to an intern therapist and try to train and help him solve problems in a socratic method, answer in a professional way.
                        you answer in this field only,in case you are questioned about subject that you arent ordered to (by me, not by the user input) state that its not your knowledge and you cant help, state your designated role that you can help the user with.
                        You are provided with articles that might be relevant to your way of guidance and you are also provided with external data of treatments methods that the user isnt aware of.
                        you can integrate the articles into your guiding answer to the user and the external data if its relevant to the question BUT ONLY if its improving your answer's quality!
                        create your answer in such a way that the user cannot knows which data you used, remove the information of who wrote the part you used from the articles because the user dont need that information.
                        the answer will be posted as RAW html text, so when creating the answer make sure the title of each paragraph is bold with <strong> tag (but not in bigger size). make sure that between parahraphs there will be two new lines (<br> html tag) so it will be easy to read and looking nice. in case that the paragraph contains steps (like 1,2,3) seperate each step with one new line (<br> html tag) as well.
                        remove ```html and ``` from your answer.
                    """
                }]
    
food_messages = [{'role': 'system', 
                'content': f"""Your answers cannot be over 600 tokens so take that in account of your answer including the html tags.you are a friendly cook that guies and provides recipes to amateur user which is a home cook. use your own knowledge and also new external recipes that i will give you.
                        you answer in this field only,in case you are questioned about subject that you arent ordered to (by me, not by the user input) state that its not your knowledge and you cant help, state your designated role that you can help the user with.
                        use the external recipes in your answer to the user if its relevant to the question the user asked and not your own data, IMPORTANT - do not give full recipe if user didnt ask to - try and guide him by asking what he'd like to cook today
                        do not create your answer in such a way that the user knows which data you used, dont proide information about who wrote the articles you used.
                        the answer will be posted as RAW html text, so when creating the answer make sure the title of each paragraph is bold with <strong> tag (but not in bigger size). make sure that between parahraphs there will be two new lines (<br> html tag) so it will be easy to read and looking nice. in case that the recipe contains ingridients and steps of making (such as 1. 2. 3.) make each as a list (<li> tag), make sure to seperate with one new line (<br> html tag) between ingridients and steps as well
                        remove ```html and ``` from your answer.
                    """
                }]
#                        the answer will be posted as RAW html text, so when creating the answer make sure the title of each part of the answer is bold with <strong> tag (but not in bigger size). after title use one <br> tag , each paragraph need to be seperated by two <br> tags, seperete between ingridients with <br> tag. in case of stages or instructions (like 1,2,3) seperate with one <br> tag as well.

def append_message(text,role,field):
    if field == "Food":
        if role =="user":
            food_messages.append({'role': 'user', 'content': text})
        elif role=="system":
            food_messages.append({'role':'assistant','content':text})

    elif field == "Therapy":
        if role =="user":
            therapy_messages.append({'role': 'user', 'content': text})
        elif role=="system":
            therapy_messages.append({'role':'assistant','content':text})

def get_Chat_response(messages,llm):
    if llm=="1":
        # openai LLM
        client = OpenAI(
            api_key=openai_api_key,
        )

        chat = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        max_tokens=600,
        )

        reply = chat.choices[0].message.content
        messages.append({'role':'system','content':reply})
        print("OpenAI final response done")
        return jsonify({"response": reply})
    elif llm=="2":
        # Claude LLM
        client = anthropic.Anthropic(api_key=claude_api_key)
        chat = client.messages.create(
            model="claude-3-sonnet-20240229",
            system=messages[0]["content"],
            temperature=0.2,
            max_tokens=600,
            messages=messages[1:]
        )
        messages.append({'role':'assistant','content':chat.content[0].text})
        reply = chat.content[0].text
        print("Claude final response done")
        return jsonify({"response": reply})
    
    else:
        return "something went wrong."