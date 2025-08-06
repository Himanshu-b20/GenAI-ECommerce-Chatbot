from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
small_talk_client = Groq()


def small_talk_chain(query):
    prompt = f''' Assume you are working as a customer care agent and your name is 'Askie'. Given below the query from customer, generate the answer to the customer. Be polite and do not make things up.

    Query : {query}

    '''
    completion = small_talk_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content
