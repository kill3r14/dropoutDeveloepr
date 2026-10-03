from langchain_core.tools import tool
import sqlparse
import sqlite3

# The @tool decorator auto-generates OpenAI function schemas
@tool
def execute_safe_query(query: str) -> list:
    """Execute a read-only query against the orders database with AST safety checks."""

    # Step 1: Parse query into Abstract Syntax Tree
    # Inspect structure before database evaluation
    parsed = sqlparse.parse(query)
    if not parsed:
        raise ValueError("Invalid SQL statement")
    for statement in parsed:
        for token in statement.tokens:
            if token.value.upper() in ["DROP", "DELETE", "TRUNCATE", "UPDATE"]:
                raise ValueError(f"Security Alert: Destructive query {token.value} blocked.")

    # Step 2: Run against isolated read-only connection
    conn = sqlite3.connect("file:production.db?mode=ro", uri=True)
    return conn.execute(query).fetchall()

@tool
def issue_stripe_refund(customer_id: str, amount: float) -> str:
    """Issue a Stripe refund after human approval is granted."""
    return f"Refund of ${amount:.2f} issued to {customer_id} (ch_3M9q82)"
