import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from src.helper import get_embeddings, get_vector_store
from src.prompt import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/ask": {"origins": "*"}})

# ── Initialize RAG components once at startup ────────────────
print("Loading embedding model ...")
embedding = get_embeddings()

print("Connecting to ChromaDB Cloud ...")
vector_store = get_vector_store(embedding)

print("Setting up Groq LLM ...")
llm = ChatGroq(
    model=os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant"),
    temperature=0.4,
    groq_api_key=os.environ.get("GROQ_API_KEY"),
)

PROMPT = PromptTemplate(
    template=SYSTEM_PROMPT,
    input_variables=["context", "question"],
)

retriever = vector_store.as_retriever(search_kwargs={"k": 4})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Modern LCEL approach to RAG (bypasses deprecated langchain.chains entirely)
rag_chain_from_docs = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | PROMPT
    | llm
    | StrOutputParser()
)

qa_chain = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
).assign(answer=rag_chain_from_docs)

print("[OK] Medical Chatbot ready!")


# ── Routes ───────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question.", "sources": []})

    try:
        result = qa_chain.invoke(question)
        answer = result["answer"]

        sources = []
        for doc in result.get("context", []):
            src = doc.metadata.get("source", "Unknown")
            sources.append(src)
        sources = list(set(sources))

        return jsonify({"answer": answer, "sources": sources})

    except Exception as e:
        return jsonify({"answer": f"An error occurred: {str(e)}", "sources": []})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
