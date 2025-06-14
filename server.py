from flask import Flask, request, jsonify
import os

# Vector store and embeddings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Groq LLM integration
from langchain_groq import ChatGroq

from langchain.chains import RetrievalQA
from flask_cors import CORS

# Set your Groq API key
os.environ["GROQ_API_KEY"] = "<YOUR_GROQ_API_KEY>"  # <-- Replace with your real Groq API key

# Chroma vector store directory
persist_directory = "chroma"

# Embedding and Vector Store
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)

# LLM (Groq Llama 3.1) and Retriever
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # or "llama3-8b-8192" if available
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    groq_api_key=os.environ["GROQ_API_KEY"]
)
retriever = vectordb.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Flask app setup
app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        print(f"🔹 User input: {user_message}")
        if not user_message:
            return jsonify({"message": "Empty message"}), 400
        response = qa_chain.run(user_message)
        print(f"✅ RAG response: {response}")
        return jsonify({"message": response})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
