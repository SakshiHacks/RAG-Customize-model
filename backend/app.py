from flask import Flask, request, jsonify
from backend.rag.rag_chain import get_rag_chain

app = Flask(__name__)

rag_chain = None  # lazy-loaded


def initialize_rag():
    global rag_chain
    if rag_chain is None:
        rag_chain = get_rag_chain()


@app.route("/", methods=["GET"])
def home():
    return {"status": "OK"}


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    initialize_rag()
    answer = rag_chain.run(question)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    initialize_rag()
    app.run(host="127.0.0.1", port=5000, debug=True)
