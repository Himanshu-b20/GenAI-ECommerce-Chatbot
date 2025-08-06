import pandas as pd
from pathlib import Path
import chromadb
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()
faq_path = Path(__file__).parent / "resources/ecommerce_faq.csv"
chroma_client = chromadb.Client()
groq_client = Groq()
collection_name = "faqs"


def ingest_data(filepath):
    if collection_name not in [c.name for c in chroma_client.list_collections()]:
        collection = chroma_client.get_or_create_collection(
            name=collection_name
        )
        df = pd.read_csv(filepath)
        docs = df['Question'].to_list()
        metadata = [{'answer':  ans} for ans in df['Answer'].to_list()]
        ids = [f'id_{i}' for i in range(len(docs))]

        collection.add(
            documents= docs,
            metadatas= metadata,
            ids = ids
        )
    else:
        print("Collection Already Exists!!")

def get_relevant_qa(query):
    collection = chroma_client.get_collection(name= collection_name)
    result = collection.query(
        query_texts=[query],
        n_results=2
    )
    return result

def faq_chain(query):
    result = get_relevant_qa(query)

    context = ''.join([r.get('answer') for r in result['metadatas'][0]])
    answer = generate_answer(query, context)
    return answer

def generate_answer(query, context):

    prompt = f''' Assume you are working as a customer care agent. Given the question and context below, generate the answer to the customer based on the context only. Do not make things up.
    
    QUESTION : {query}
    
    CONTEXT: {context}
    
    '''
    completion = groq_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

if __name__=='__main__':
    ingest_data(faq_path)
    query='Do you take cash as a payment option?'
    # print(get_relevant_qa(query))
    result = faq_chain(query)
    print(result)