import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_route(query):
    score_list_faq = []
    score_list_small = []
    score_list_sql = []
    utterances_faq = [
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "What payment methods are accepted?",
        "How can i track my order?"
        "How long does it take to process a refund?",
        "Are there any ongoing sales or promotions?",
        "what is the return policy of the products?",
        "do I get discount with the HDFC credit card?",
        "what payment methods are accepted?",
        "how long does it take to process a refund?",
        "are there any ongoing sales or promotions?",
        "how can i track my order?"
    ]

    utterances_small = [
        "How are you?",
        "What is your name?",
        "Are you a robot?",
        "What are you?",
        "What do you do?",
        "Thanks!"
        "Thanks for help!"
        "how are you?",
        "what is your name?",
        "are you a robot?",
        "what are you?",
        "what do you do?",
        "thanks!"
        "thanks for help!"
    ]

    utterances_sql = [
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
        "All shoes with rating more than 4.",
        "All Nike shoes with rating greater than 4.",
        "i want to buy nike shoes that have 50% discount.",
        "are there any shoes under Rs. 3000?",
        "do you have formal shoes in size 9?",
        "are there any Puma shoes on sale?",
        "what is the price of puma running shoes?",
        "all shoes with rating more than 4.",
        "all Nike shoes with rating greater than 4."
    ]


    query_vec = model.encode(query, convert_to_numpy=True)

    for utterance_f, utterance_s, utterance_sql in zip(utterances_faq, utterances_small, utterances_sql):
        u_vec_faq = model.encode(utterance_f, convert_to_numpy=True)
        score_faq = cosine_sim(query_vec, u_vec_faq)

        u_vec_small = model.encode(utterance_s, convert_to_numpy=True)
        score_small = cosine_sim(query_vec, u_vec_small)

        u_vec_sql = model.encode(utterance_sql, convert_to_numpy=True)
        score_sql = cosine_sim(query_vec, u_vec_sql)

        score_list_faq.append(score_faq)
        score_list_small.append(score_small)
        score_list_sql.append(score_sql)


    if max(score_list_faq) >= 0.6:
        return 'faq'
    if max(score_list_small) >=0.6:
        return 'small-talk'
    if max(score_list_sql) >=0.6:
        return 'sql'

    return 'None'


if __name__ == "__main__":
    query = "your name?"
    print(get_route(query))

