from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

TRIAGE_FILE = ROOT / "outputs" / "ticket_triage.csv"
SEGMENTS_FILE = ROOT / "outputs" / "customer_segments.csv"
OUTPUT_FILE = ROOT / "outputs" / "ticket_routing.csv"
SUMMARY_FILE = ROOT / "outputs" / "token_budget_summary.csv"

# Configurable token budget.
# Change this value if your assignment specifies another limit.
TOKEN_BUDGET = 15000


def main():
    # Check required input files.
    for file in [TRIAGE_FILE, SEGMENTS_FILE]:
        if not file.exists():
            raise FileNotFoundError(f"Required file not found: {file}")

    tickets = pd.read_csv(TRIAGE_FILE)
    customers = pd.read_csv(SEGMENTS_FILE)

    # Keep only the columns needed from customer segmentation.
    customers = customers[
        ["customer_id", "frequency", "monetary", "segment"]
    ].copy()

    # Join ticket details with customer information.
    routed = tickets.merge(
        customers,
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    # Assign the responsible support team.
    team_map = {
        "fraud": "Trust and Safety",
        "billing": "Billing Support",
        "delivery": "Delivery Support",
        "technical": "Technical Support",
    }

    routed["assigned_team"] = (
        routed["category"].map(team_map).fillna("General Support")
    )

    # Set initial priority.
    priority_map = {
        "fraud": "P1",
        "billing": "P2",
        "delivery": "P2",
        "technical": "P2",
    }

    routed["priority"] = routed["category"].map(priority_map).fillna("P3")

    # Flag customers whose monetary value is in the top 25%.
    valid_monetary = customers["monetary"].dropna()

    if not valid_monetary.empty:
        high_value_threshold = valid_monetary.quantile(0.75)
    else:
        high_value_threshold = float("inf")

    routed["high_value_customer"] = (
        routed["monetary"].fillna(0) >= high_value_threshold
    )

    # Escalate high-value customers' non-fraud tickets to P1.
    # Fraud tickets already have P1 priority.
    high_value_mask = (
        routed["high_value_customer"]
        & (routed["category"] != "fraud")
        & (routed["status"] == "success")
    )

    routed.loc[high_value_mask, "priority"] = "P1"

    # Track tokens used by the ticket-classification process.
    token_columns = [
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
    ]

    for column in token_columns:
        routed[column] = pd.to_numeric(
            routed[column], errors="coerce"
        ).fillna(0)

    total_tokens = int(routed["total_tokens"].sum())
    remaining_tokens = max(TOKEN_BUDGET - total_tokens, 0)

    summary = pd.DataFrame([{
        "token_budget": TOKEN_BUDGET,
        "prompt_tokens": int(routed["prompt_tokens"].sum()),
        "completion_tokens": int(routed["completion_tokens"].sum()),
        "total_tokens": total_tokens,
        "remaining_tokens": remaining_tokens,
        "budget_exceeded": total_tokens > TOKEN_BUDGET,
        "tickets_processed": len(routed),
        "successful_tickets": int(
            (routed["status"] == "success").sum()
        ),
        "failed_tickets": int(
            (routed["status"] != "success").sum()
        ),
    }])

    routed.to_csv(OUTPUT_FILE, index=False)
    summary.to_csv(SUMMARY_FILE, index=False)

    print("Ticket routing completed.")
    print(f"Tickets processed: {len(routed)}")
    print("\nAssigned teams:")
    print(routed["assigned_team"].value_counts().to_string())

    print("\nPriority distribution:")
    print(routed["priority"].value_counts().to_string())

    print("\nToken budget summary:")
    print(summary.to_string(index=False))

    print(f"\nRouting output: {OUTPUT_FILE}")
    print(f"Budget summary: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()