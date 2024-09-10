from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv
import anthropic
import os


load_dotenv()
openai_api_key = os.getenv('OPENAI_KEY')
pinecone_api_key = os.getenv('PINECONE_KEY')
claude_api_key = os.getenv('CLAUDE_KEY')

pc = Pinecone(api_key=pinecone_api_key)
namespace = "data1"
index_name = "embedata"
index = pc.Index(index_name)

client = OpenAI(api_key=openai_api_key)

# our embedding model - embedding dimensions is 1536
embeddings = OpenAIEmbeddings(  
    model="text-embedding-3-small",
    openai_api_key=openai_api_key
)  

def context_retrieve(text, name):
    if name == "cases":
        pc = Pinecone(api_key=pinecone_api_key)
        namespace = "data1"
        index_name = "embedata"
        index = pc.Index(index_name)

        # embedd user text
        vector = client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
                encoding_format="float"
                ).data[0].embedding
        
        # returns the metadata that related to the user embedded text (k=3)
        results = index.query(
                namespace=namespace,
                vector=vector,
                top_k=3,
                include_metadata=True,
                )

        context = []
        for result in results['matches']:
            context.append(result['metadata']['text'])
            # print(f"{round(result['score'], 2)}: {result['metadata']['text']}")
            # print()
        print("Articles / use cases RAG finished")
        return context
    
    elif name == "articles":
        pc = Pinecone(api_key=pinecone_api_key)
        namespace = "data1"
        index_name = "training"
        index = pc.Index(index_name)

        # embedd user text
        vector = client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
                encoding_format="float"
                ).data[0].embedding
        
        # returns the metadata that related to the user embedded text (k=3)
        results = index.query(
                namespace=namespace,
                vector=vector,
                top_k=3,
                include_metadata=True,
                )

        context = []
        for result in results['matches']:
            context.append(result['metadata']['text'])
            # print(f"{round(result['score'], 2)}: {result['metadata']['text']}")
        print("Guidance data RAG finished")
        return context
    
    elif name == "recipes":
        pc = Pinecone(api_key=pinecone_api_key)
        namespace = "data1"
        index_name = "food"
        index = pc.Index(index_name)

        # embedd user text
        vector = client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
                encoding_format="float"
                ).data[0].embedding
        
        # returns the metadata that related to the user embedded text (k=3)
        results = index.query(
                namespace=namespace,
                vector=vector,
                top_k=3,
                include_metadata=True,
                )

        context = []
        for result in results['matches']:
            context.append(result['metadata']['text'])
            # print(f"{round(result['score'], 2)}: {result['metadata']['text']}")
            # print()
        print("Food RAG finished")
        return context


def guidance_generation(text,llm):
    msg = [{'role': 'system', 
             'content': f"""you are a occupational therapy assistant that provies a guided training to an intern therapist and try to train and help him solve problems in a socratic method,
                    You are provided with the user question, you will return the way of guidance or training you think is right for this question.
                    Your answer is used to extract related articles about guided traning in a socratic method using RAG method with external vector db.
                    intern input = {text}
                """
             }]
    if llm=="1":
        # openai LLM
        client = OpenAI(
            api_key=openai_api_key,
        )

        chat = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=msg,
        max_tokens=500,
        )

        reply = chat.choices[0].message.content
        print("OpenAI guidance choice response done")
        return reply
    
    elif llm=="2":
        # Claude LLM
        client = anthropic.Anthropic(api_key=claude_api_key)
        chat = client.messages.create(
            model="claude-3-sonnet-20240229",
            system=msg[0]["content"],
            max_tokens=350,
            messages=[{"role": "user", "content": text}]
        )
        reply = chat.content[0].text
        print("Claude guidance choice response done")
        return reply
    else:
        return "something went wrong."