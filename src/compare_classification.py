import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import mock_llm

INPUT_PATH = ROOT / "data" / "raw" / "tickets.csv"
OUTPUT_PATH = ROOT / "outputs" / "classification_comparison.csv"

ALLOWED_CATEGORIES = {"billing", "delivery", "technical", "fraud"}

ZERO_SHOT_PROMPT = """
CLASSIFY support tickets.
Return valid JSON with category and reason.
Allowed categories: billing, delivery, technical, fraud.
"""

FEW_SHOT_PROMPT = """
CLASSIFY support tickets.
EXAMPLES:
Ticket: My invoice shows the wrong amount.
Output: {"category":"billing","reason":"invoice issue"}

Ticket: My package has not arrived.
Output: {"category":"delivery","reason":"delivery issue"}

Ticket: The app crashes when I log in.
Output: {"category":"technical","reason":"app issue"}

Ticket: Someone made an unauthorized transaction.
Output: {"category":"fraud","reason":"unauthorized transaction"}

Return valid JSON with category and reason.
Allowed categories: billing, delivery, technical, fraud.
"""


def predict(text, system_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": str(text)},
    ]

    for _ in range(4):
        try:
            response = mock_llm.chat(messages)
            result = json.loads(response.choices[0].message.content)

            if (
                isinstance(result, dict)
                and result.get("category") in ALLOWED_CATEGORIES
                and isinstance(result.get("reason"), str)
            ):
                return result["category"]

        except (mock_llm.TransientLLMError, json.JSONDecodeError, TypeError):
            continue

    return "unclassified"


def main():
    tickets = pd.read_csv(INPUT_PATH).fillna("")
    results = []

    for mode, prompt in [
        ("zero_shot", ZERO_SHOT_PROMPT),
        ("few_shot", FEW_SHOT_PROMPT),
    ]:
        mock_llm.reset()

        for _, row in tickets.iterrows():
            prediction = predict(row["text"], prompt)

            results.append({
                "ticket_id": row["ticket_id"],
                "mode": mode,
                "true_category": row["true_category"],
                "predicted_category": prediction,
            })

    output = pd.DataFrame(results)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT_PATH, index=False)

    for mode in ["zero_shot", "few_shot"]:
        subset = output[output["mode"] == mode]
        accuracy = accuracy_score(
            subset["true_category"],
            subset["predicted_category"],
        )

        print(f"\n{mode.upper()} accuracy: {accuracy:.4f}")
        print(
            classification_report(
                subset["true_category"],
                subset["predicted_category"],
                labels=sorted(ALLOWED_CATEGORIES),
                zero_division=0,
            )
        )

    print(f"Saved comparison: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()