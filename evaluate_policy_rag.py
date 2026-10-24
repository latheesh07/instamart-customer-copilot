from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from policy_rag import answer_question


TEST_CASES = [
    {
        "question": "Can cancelled orders receive a refund?",
        "expected": "cancelled",
        "source": "refund_policy.txt",
    },
    {
        "question": "What happens if delivery takes more than 45 minutes?",
        "expected": "full refund",
        "source": "refund_policy.txt",
    },
    {
        "question": "Who approves refunds above INR 1000?",
        "expected": "human",
        "source": "refund_policy.txt",
    },
    {
        "question": "How long does a refund take?",
        "expected": "5 working days",
        "source": "refund_policy.txt",
    },
    {
        "question": "When should a refund request be raised?",
        "expected": "7 days",
        "source": "refund_policy.txt",
    },
    {
        "question": "What is the delivery fee for orders below INR 199?",
        "expected": "25",
        "source": "delivery_policy.txt",
    },
    {
        "question": "Which cities are supported?",
        "expected": "chennai",
        "source": "delivery_policy.txt",
    },
    {
        "question": "How many times does the rider contact the customer?",
        "expected": "twice",
        "source": "delivery_policy.txt",
    },
]


def main():
    results = []

    for number, test in enumerate(TEST_CASES, start=1):
        response = answer_question(test["question"])

        answer = response["answer"] or ""
        answer_lower = answer.lower()
        source_found = test["source"] in response["sources"]

        passed = (
            test["expected"].lower() in answer_lower
            and source_found
        )

        results.append({
            "test": number,
            "question": test["question"],
            "answer": answer,
            "expected_keyword": test["expected"],
            "expected_source": test["source"],
            "source_found": source_found,
            "passed": passed,
            "total_tokens": response["total_tokens"],
        })

        print(f"\nTest {number}: {'PASS' if passed else 'FAIL'}")
        print(f"Question: {test['question']}")
        print(f"Answer: {answer}")
        print(f"Sources: {response['sources']}")

    import pandas as pd

    output = ROOT / "outputs" / "policy_rag_evaluation.csv"
    output.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(results)
    df.to_csv(output, index=False)

    passed_count = int(df["passed"].sum())

    print("\n========== EVALUATION SUMMARY ==========")
    print(f"Total tests: {len(df)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {len(df) - passed_count}")
    print(f"Pass rate: {passed_count / len(df) * 100:.2f}%")
    print(f"Total tokens: {int(df['total_tokens'].sum())}")
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
