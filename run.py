import sqlite3
from agent.tools import execute_safe_query
from agent.graph import app

# 0. Initialize mock production.db orders table
conn = sqlite3.connect("production.db")
conn.execute("CREATE TABLE IF NOT EXISTS orders (order_id TEXT, customer_id TEXT, amount REAL)")
conn.commit()
conn.close()

print("=== 1. Testing AST SQL Firewall ===")
try:
    execute_safe_query.invoke({"query": "DROP TABLE orders;"})
except ValueError as e:
    print(f"[AST FIREWALL PASS] Blocked destructive query -> {e}\n")

print("=== 2. Running Incident Investigation (Thread INC-8820) ===")
config = {"configurable": {"thread_id": "INC-8820"}}
initial_state = {
    "incident_id": "INC-8820",
    "customer_id": "customer_9021",
    "discrepancy_amount": 149.00,
    "messages": [],
}

result = app.invoke(initial_state, config=config)
snapshot = app.get_state(config)
print(f"\n[BREAKPOINT HALTED] Next node waiting in queue: {snapshot.next}")
print(f"[CHECKPOINT STATE] order_status={snapshot.values.get('order_status')}, discrepancy=${snapshot.values.get('discrepancy_amount'):.2f}\n")

print("=== 3. Simulating Operator Approval & Resuming from SQLite Checkpointer ===")
resumed_result = app.invoke(None, config=config)
final_snapshot = app.get_state(config)
print(f"\n[FINAL STATE] order_status={final_snapshot.values.get('order_status')}, approval_granted={final_snapshot.values.get('approval_granted')}, next={final_snapshot.next}")
