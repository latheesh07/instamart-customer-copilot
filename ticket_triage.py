import json
import re
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import mock_llm

INPUT_PATH = ROOT / "data" / "raw" / "tickets.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "ticket_triage.csv"

ALLOWED_CATEGORIES = {"billing", "delivery", "technical", "fraud"}

SYSTEM_PROMPT = """
CLASSIFY customer support tickets.
Return only valid JSON with exactly these fields:
category and reason.
Allowed categories: billing, delivery, technical, fraud.
"""


def redact_pii(text):
    """Redact phone numbers and order IDs before sending text to the LLM."""
    text = str(text)

    text = re.sub(
        r"\bORD-\d{6}\b",
        "[REDACTED_ORDER_ID]",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"(?<!\d)(?:\+?91[- ]?)?[6-9]\d{9}(?!\d)",
        "[REDACTED_PHONE]",
        text,
    )

    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "[REDACTED_EMAIL]",
        text,
    )

    return text


def classify_ticket(text, max_attempts=4):
    """Classify a ticket with retries for transient and invalid responses."""
    safe_text = redact_pii(text)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": safe_text},
    ]

    last_error = "Unknown classification error"

    for attempt in range(1, max_attempts + 1):
        try:
            response = mock_llm.chat(messages)
            content = response.choices[0].message.content

            if not content:
                raise ValueError("Empty LLM response")

            result = json.loads(content)

            if not isinstance(result, dict):
                raise ValueError("Response must be a JSON object")

            if set(result.keys()) != {"category", "reason"}:
                raise ValueError("Unexpected JSON fields")

            category = result["category"]

            if category not in ALLOWED_CATEGORIES:
                raise ValueError(f"Invalid category: {category}")

            if not isinstance(result["reason"], str):
                raise ValueError("Reason must be a string")

            return {
                "category": category,
                "reason": result["reason"],
                "attempts": attempt,
                "status": "success",
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

        except mock_llm.TransientLLMError as exc:
            last_error = str(exc)

        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            last_error = str(exc)

        if attempt < max_attempts:
            time.sleep(0.05)

    return {
        "category": "unclassified",
        "reason": last_error,
        "attempts": max_attempts,
        "status": "failed",
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    tickets = pd.read_csv(INPUT_PATH).fillna("")
    mock_llm.reset()

    results = []

    for _, row in tickets.iterrows():
        result = classify_ticket(row["text"])

        results.append({
            "ticket_id": row["ticket_id"],
            "customer_id": row["customer_id"],
            "order_id": row["order_id"],
            "redacted_text": redact_pii(row["text"]),
            "true_category": row["true_category"],
            **result,
        })

    output = pd.DataFrame(results)
    output.to_csv(OUTPUT_PATH, index=False)

    print(f"Tickets processed: {len(output)}")
    print(f"Successful classifications: {(output['status'] == 'success').sum()}")
    print(f"Failed classifications: {(output['status'] == 'failed').sum()}")

    print("\nPredicted category counts:")
    print(output["category"].value_counts().to_string())

    print("\nRetry attempts:")
    print(output["attempts"].value_counts().sort_index().to_string())

    print("\nToken usage:")
    print(f"Total tokens: {output['total_tokens'].sum()}")

    print(f"\nSaved output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()