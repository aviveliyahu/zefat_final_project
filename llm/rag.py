from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
openai_api_key = os.getenv('OPENAI_KEY')
pinecone_api_key = os.getenv('PINECONE_KEY')

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

def context_retrieve(text):
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
    return context