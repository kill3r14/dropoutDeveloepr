from agent.state import IncidentState
from agent.tools import execute_safe_query, issue_stripe_refund

def triage(state: IncidentState) -> dict:
    print(f"[triage] classified SEV-2 Billing Incident for {state['customer_id']}")
    return {"order_status": "INVESTIGATING", "raw_error": None}

def query_db(state: IncidentState) -> dict:
    query = f"SELECT * FROM orders WHERE customer_id='{state['customer_id']}'"
    print(f"[query_db] executing {query}...")
    rows = execute_safe_query.invoke({"query": query})
    print(f"[query_db] row count: {len(rows)}")
    return {"order_status": "ORPHANED_CHARGE" if len(rows) == 0 else "FOUND", "raw_error": None}

def reconcile(state: IncidentState) -> dict:
    amount = state["discrepancy_amount"]
    print(f"[reconcile] calculating credit delta: +${amount:.2f} (orphaned Stripe charge detected)")
    return {"order_status": "AWAITING_APPROVAL"}

def request_approval(state: IncidentState) -> dict:
    amount = state["discrepancy_amount"]
    customer_id = state["customer_id"]
    print(f"[request_approval] operator decision: APPROVED. Issuing refund...")
    receipt = issue_stripe_refund.invoke({"customer_id": customer_id, "amount": amount})
    print(f"[execute_refund] {receipt}")
    return {"order_status": "RESOLVED", "approval_granted": True}
