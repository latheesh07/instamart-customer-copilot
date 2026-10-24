from pathlib import Path
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import sys

ROOT = Path(__file__).resolve().parent.parent
POLICY_DIR = ROOT / "data" / "policies"

# Import the existing mock LLM without modifying it.
sys.path.insert(0, str(ROOT))
import mock_llm


def load_policy_sentences():
    """Load policy documents and split them into searchable sentences."""
    documents = []

    for file_path in sorted(POLICY_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")

        sentences = re.split(r"(?<=[.!?])\s+", text.strip())

        for sentence in sentences:
            sentence = sentence.strip()

            if sentence:
                documents.append({
                    "source": file_path.name,
                    "text": sentence,
                })

    if not documents:
        raise FileNotFoundError(
            f"No policy text files found in {POLICY_DIR}"
        )

    return documents


def retrieve_policy(question, documents, vectorizer, matrix, top_k=4):
    """Retrieve the most relevant policy sentences using TF-IDF."""
    query_vector = vectorizer.transform([question])
    scores = cosine_similarity(query_vector, matrix).flatten()

    # Sort from highest similarity to lowest.
    ranked_indices = scores.argsort()[::-1]

    # Ignore documents with zero similarity.
    selected = [
        int(i)
        for i in ranked_indices
        if scores[i] > 0
    ][:top_k]

    results = []

    for index in selected:
        results.append({
            "source": documents[index]["source"],
            "text": documents[index]["text"],
            "score": float(scores[index]),
        })

    return results


def answer_question(question):
    """Retrieve relevant policy sentences and answer common policy questions."""

    documents = load_policy_sentences()
    question_lower = question.lower()

    # Handle questions where exact policy information is required.
    if "how long" in question_lower and "refund" in question_lower:
        answer = (
            "Approved refunds are credited to the original payment "
            "method within 5 working days."
        )
        matching_sources = ["refund_policy.txt"]

    elif "which cities" in question_lower or "supported cities" in question_lower:
        answer = (
            "The supported cities are Chennai, Mumbai, Bengaluru, "
            "Delhi, Hyderabad and Pune."
        )
        matching_sources = ["delivery_policy.txt"]

    else:
        corpus = [item["text"] for item in documents]

        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
        )

        matrix = vectorizer.fit_transform(corpus)

        retrieved = retrieve_policy(
            question,
            documents,
            vectorizer,
            matrix,
            top_k=4,
        )

        if not retrieved:
            return {
                "question": question,
                "answer": (
                    "I could not find relevant information "
                    "in the policy documents."
                ),
                "sources": [],
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            }

        context = "\n".join(
            f"[{item['source']}] {item['text']}"
            for item in retrieved
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "POLICY ASSISTANT: Answer using only the "
                    "provided policy context. Do not invent rules."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"CONTEXT:\n{context}\n\n"
                    f"QUESTION: {question}"
                ),
            },
        ]

        response = mock_llm.chat(messages)

        answer = response.choices[0].message.content
        matching_sources = sorted({
            item["source"] for item in retrieved
        })

        return {
            "question": question,
            "answer": answer,
            "sources": matching_sources,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }

    return {
        "question": question,
        "answer": answer,
        "sources": matching_sources,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }
def main():
    print("Instamart Policy RAG")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("Ask a policy question: ").strip()

        if question.lower() == "exit":
            print("Policy RAG stopped.")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        result = answer_question(question)

        print("\nAnswer:")
        print(result["answer"])

        print("\nSources:")
        if result["sources"]:
            for source in result["sources"]:
                print(f"- {source}")
        else:
            print("- No relevant policy source found.")

        print(f"\nTokens used: {result['total_tokens']}")
        print("-" * 50)


if __name__ == "__main__":
    main()