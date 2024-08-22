from pinecone import Pinecone
from openai import OpenAI

openai_key = "sk-proj-mf2KofruPMUsxcGSC3WYT3BlbkFJwwAyFhNEE89NTEsoz7Ow"
pc = Pinecone(api_key="c02bf718-1e95-4782-9344-3a06f48c5e86")

client = OpenAI(api_key=openai_key)

namespace = "data1"
index_name = "training"
index = pc.Index(index_name)

def upsert_data(text):
    #data = embeddings.embed_documents(text)[1]
    next_id = 0
    for ids in index.list(namespace=namespace):
          id = ids
          last_id = id[-1]
          next_id = int(last_id)+1

    chunks = []

    for i in range(len(text)):
        data = client.embeddings.create(
            model="text-embedding-3-small",
            input=text[i],
            encoding_format="float"
            ).data[0].embedding
          
        chunks.append({"id":str(next_id),"values":data,"metadata":{"text":text[i]}})
        print(f"appeneded {i}")
        next_id = next_id+1

    index.upsert(
         vectors=chunks,
         namespace=namespace
     )
    print("Data uploaded successfully.")