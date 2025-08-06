# 🤖 E-Commerce AI Chatbot (with Semantic Routing + Groq Cloud + LLaMA 3.3 70B)
This project is an AI-powered chatbot built for e-commerce platforms to automate and enhance customer interactions. It can handle FAQs, product-related queries, and casual small talk using a semantic routing system combined with a high-performance large language model (LLM).

## 🔍 How It Works
**Semantic Routing (using sentence transformer) :**
 Incoming user messages are semantically analyzed and classified into three categories:
- FAQs (e.g., "What’s the return policy?")
- Product Queries (e.g., "All Nike shoes with rating higher than 4.8")
- Small Talk (e.g., "Hey, whats your name?")

This classification ensures that each query type is handled with the right logic and context.

**LLM-Powered Responses via Groq :**
 Once routed, the query is sent to Groq Cloud, using Meta's LLaMA-3.3-70B-Versatile model for generating fast, accurate, and context-aware responses. Groq’s ultra-low-latency architecture enables real-time conversations at scale.

## 🛠️ Tech Stack
- **Python**
- **ChromaDB**
- **SQLite DB**
- **Groq + LLM (model=llama-3.3-70b-versatile)**
- **Sentence Embeddings (using sentence-transformers/all-MiniLM-L6-v2)**

## 🧪 Setup & Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Himanshu-b20/GenAI-ECommerce-Chatbot.git
   ```
2. **Install dependencies:**:   
   ```commandline
    pip install -r requirements.txt
   ```
3. **Create a .env file and add your keys:**:   
   ```commandline
    GROQ_API_KEY=your_groq_key
    GROQ_MODEL=llama-3.3-70b-versatile
   ```
4. **Run the Streamlit app:**:   
   ```commandline
    streamlit run app/main.py
   ```
