import sqlite3
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
from pathlib import Path
import re


load_dotenv()
sql_path = Path(__file__).parent / "db.sqlite"
sql_groq_client = Groq()

def run_query(query):
    if query.strip().upper().startswith('SELECT'):
        with sqlite3.connect(sql_path) as conn:
            df = pd.read_sql(query, conn)
            return df
    return None


sql_prompt = """You are an expert in understanding the database schema and generating SQL queries for a natural language question asked
pertaining to the data you have. The schema is provided in the schema tags. 
<schema> 
table: product 

fields: 
product_link - string (hyperlink to product)	
title - string (name of the product)	
brand - string (brand of the product)	
price - integer (price of the product in Indian Rupees)	
discount - float (discount on the product. 10 percent discount is represented as 0.1, 20 percent as 0.2, and such.)	
avg_rating - float (average rating of the product. Range 0-5, 5 is the highest.)	
total_ratings - integer (total number of ratings for the product)

</schema>
Make sure whenever you try to search for the brand name, the name can be in any case. Also when question contains 'all shoes' or 'all shoe' in any case upper or lower add title LIKE '%shoes%' in sql query.
So, make sure to use %LIKE% to find the brand in condition. Never use "ILIKE". 
Create a single SQL query for the question provided. If you dont get relevant information to generate sql query from question just return 'Cant generate the query' without 
The query should have all the fields in SELECT clause (i.e. SELECT *)

Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL></SQL> tags. If you dont get relevant information to generate sql query from question just return 'Cant generate the query' without any SQL tags"""


comprehension_prompt = """You are an expert in understanding the context of the question and replying based on the data pertaining to the question provided. You will be provided with Question: and Data:. The data will be in the form of an array or a dataframe or dict. Reply based on only the data provided as Data for answering the question asked as Question. Do not write anything like 'Based on the data' or any other technical words. Just a plain simple natural language response.
The Data would always be in context to the question asked. For example is the question is “What is the average rating?” and data is “4.3”, then answer should be “The average rating for the product is 4.3”. So make sure the response is curated with the question and data. Make sure to note the column names to have some context, if needed, for your response.
There can also be cases where you are given an entire dataframe in the Data: field. Always remember that the data field contains the answer of the question asked. All you need to do is to always reply in the following format when asked about a product: 
Produt title, price in indian rupees, discount, and rating, and then product link. Take care that all the products are listed in list format, one line after the other. Not as a paragraph. 
For example:
1. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
2. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
3. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>

"""
def generate_sql_query(question):

    completion = sql_groq_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[
            {
                "role": "system",
                "content": sql_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.2
    )
    return completion.choices[0].message.content


def data_comprehension(question, context):

    completion = sql_groq_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[
            {
                "role": "system",
                "content": comprehension_prompt
            },
            {
                "role": "user",
                "content": f'Question: {question}, Data: {context}'
            }
        ],
        temperature=0.2
    )
    return completion.choices[0].message.content

def sql_chain(question):
    sql_query = generate_sql_query(question)
    pattern = "<SQL>(.*?)</SQL>"
    matches = re.findall(pattern, sql_query, re.DOTALL)
    if len(matches) == 0:
        return "Sorry LLM not able to generate query for your question."

    response = run_query(matches[0].strip())
    print("SQL Query..", matches[0].strip())
    if response is None:
        return "Sorry there was probelm executing the query."
    
    context = response.to_dict(orient='records')
    answer = data_comprehension(question, context)
    return answer


if __name__ == '__main__':
    # query = "SELECT * from product where brand LIKE '%nike%'"
    # df = run_query(query)
    # pass
    question = 'All Nike shoes with rating higher than 4.8'
    question2 = 'Give me Puma shoes with rating higher than 4.5 and discount more than 30%'
    answer = sql_chain(question2)
    print(answer)