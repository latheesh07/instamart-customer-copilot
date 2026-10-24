from pathlib import Path
import json
import sqlite3
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "instamart.db"
POLICY_PATH = ROOT / "data" / "policies" / "refund_policy.txt"
OUTPUT_PATH = ROOT / "outputs" / "refund_agent_log.csv"
CHECKPOINT_PATH = ROOT / "state" / "refund_agent_checkpoint.json"

sys.path.insert(0, str(ROOT))
import mock_llm


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Retrieve order details using its order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_policy",
            "description": "Retrieve the refund policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_refund",
            "description": "Calculate late-delivery refund eligibility.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_amount": {"type": "number"},
                    "delivery_minutes": {
                        "type": ["number", "null"]
                    }
                },
                "required": [
                    "order_amount",
                    "delivery_minutes"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "issue_refund",
            "description": "Simulate an approved refund.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "refund_inr": {"type": "number"}
                },
                "required": ["order_id", "refund_inr"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Request human approval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "refund_inr": {"type": "number"}
                },
                "required": ["order_id", "refund_inr"]
            }
        }
    }
]


def get_order(order_id):
    """Read order details from SQLite."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT order_id, customer_id, status,
                   order_amount, delivery_minutes
            FROM orders
            WHERE order_id = ?
            """,
            (order_id,)
        ).fetchone()

    if row is None:
        return {"error": "order_not_found"}

    return dict(row)


def search_policy(query):
    """Read the refund policy document."""
    if not POLICY_PATH.exists():
        return {"error": "refund_policy_not_found"}

    return {
        "query": query,
        "policy": POLICY_PATH.read_text(encoding="utf-8")
    }


def calculate_refund(order_amount, delivery_minutes):
    """Apply the late-delivery refund rule."""
    if delivery_minutes is None:
        return {
            "refund_inr": 0,
            "reason": "Delivery time is unavailable."
        }

    if float(delivery_minutes) > 45:
        return {
            "refund_inr": round(float(order_amount), 2),
            "reason": "Completed delivery exceeded 45 minutes."
        }

    return {
        "refund_inr": 0,
        "reason": "Delivery was within 45 minutes."
    }


def execute_tool(name, arguments):
    """Execute only approved tools."""
    if name == "get_order":
        return get_order(arguments["order_id"])

    if name == "search_policy":
        return search_policy(arguments["query"])

    if name == "calculate_refund":
        return calculate_refund(
            arguments["order_amount"],
            arguments["delivery_minutes"]
        )

    if name == "issue_refund":
        # Simulation only. No real money is transferred.
        return {
            "status": "simulated",
            "order_id": arguments["order_id"],
            "refund_inr": arguments["refund_inr"],
            "message": "No real refund was issued."
        }

    if name == "escalate_to_human":
        return {
            "status": "pending_human_approval",
            "order_id": arguments["order_id"],
            "refund_inr": arguments["refund_inr"]
        }

    return {"error": "tool_not_allowed"}


def save_checkpoint(order_id, messages, step, status):
    """Save the current agent progress."""
    CHECKPOINT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    checkpoint = {
        "order_id": order_id,
        "step": step,
        "status": status,
        "messages": messages
    }

    CHECKPOINT_PATH.write_text(
        json.dumps(checkpoint, indent=2, default=str),
        encoding="utf-8"
    )


def run_agent(order_id, max_steps=10):
    """Run the agent with bounded tool execution."""
    mock_llm.reset()

    messages = [
        {
            "role": "system",
            "content": (
                "AGENT: Handle refund requests using the provided tools. "
                "Check the order and policy before calculating a refund. "
                "All refunds are simulations only. Never claim that real "
                "money has been transferred."
            )
        },
        {
            "role": "user",
            "content": (
                f"Please check refund eligibility for order {order_id}."
            )
        }
    ]

    log = []

    for step in range(1, max_steps + 1):
        save_checkpoint(order_id, messages, step, "running")

        try:
            response = mock_llm.chat(messages, tools=TOOLS)
        except mock_llm.TransientLLMError as exc:
            result = {
                "order_id": order_id,
                "status": "error",
                "message": f"Temporary LLM error: {exc}"
            }
            save_checkpoint(order_id, messages, step, "error")
            return result, log

        choice = response.choices[0]
        message = choice.message

        if (
            choice.finish_reason != "tool_calls"
            or not message.tool_calls
        ):
            answer = message.content or "No final answer returned."

            if answer.startswith("REFUND:"):
                answer = (
                    "SIMULATION ONLY - no real refund was issued. "
                    "Eligible refund: "
                    + answer[len("REFUND:"):].strip()
                )

            result = {
                "order_id": order_id,
                "status": "completed",
                "message": answer
            }

            log.append({
                "order_id": order_id,
                "step": step,
                "tool": "final_answer",
                "result": answer
            })

            save_checkpoint(
                order_id, messages, step, "completed"
            )
            return result, log

        for tool_call in message.tool_calls:
            name = tool_call.name

            try:
                arguments = (
                    tool_call.arguments
                    if isinstance(tool_call.arguments, dict)
                    else json.loads(tool_call.arguments)
                )
            except (ValueError, TypeError):
                result = {
                    "order_id": order_id,
                    "status": "error",
                    "message": "Invalid tool arguments."
                }
                save_checkpoint(
                    order_id, messages, step, "error"
                )
                return result, log

            tool_result = execute_tool(name, arguments)

            log.append({
                "order_id": order_id,
                "step": step,
                "tool": name,
                "result": json.dumps(
                    tool_result, default=str
                )
            })

            messages.append({
                "role": "tool",
                "name": name,
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    tool_result, default=str
                )
            })

            if name == "get_order" and "error" in tool_result:
                result = {
                    "order_id": order_id,
                    "status": "not_found",
                    "message": (
                        "Order not found. No refund action taken."
                    )
                }
                save_checkpoint(
                    order_id, messages, step, "not_found"
                )
                return result, log

    result = {
        "order_id": order_id,
        "status": "stopped",
        "message": "Maximum tool steps reached; stopped safely."
    }

    save_checkpoint(
        order_id, messages, max_steps, "stopped"
    )
    return result, log


def save_log(log):
    """Append agent events to the CSV log."""
    if not log:
        return

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    new_df = pd.DataFrame(log)

    if OUTPUT_PATH.exists():
        old_df = pd.read_csv(OUTPUT_PATH)
        new_df = pd.concat(
            [old_df, new_df],
            ignore_index=True
        )

    new_df.to_csv(OUTPUT_PATH, index=False)


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    if not POLICY_PATH.exists():
        raise FileNotFoundError(
            f"Policy not found: {POLICY_PATH}"
        )

    print("Instamart Refund Agent")
    print("Simulation only; no real refund will be issued.")
    print("Type 'exit' to stop.\n")

    while True:
        try:
            order_id = input(
                "Enter order ID (e.g. ORD-000001): "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nRefund agent stopped.")
            break

        if order_id.lower() == "exit":
            print("Refund agent stopped.")
            break

        if not order_id:
            print("Please enter an order ID.\n")
            continue

        result, log = run_agent(order_id)

        print("\nResult:")
        print(json.dumps(result, indent=2))

        save_log(log)

        if log:
            print(f"\nAgent log saved: {OUTPUT_PATH}")

        print(f"Checkpoint saved: {CHECKPOINT_PATH}")
        print("-" * 50)


if __name__ == "__main__":
    main()