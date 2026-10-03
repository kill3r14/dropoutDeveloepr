# LangGuard: Autonomous AI Incident Copilot (LangGraph Full Course)

Official companion repository for the **How Tech Runs / Dropout Developer** LangChain & LangGraph Masterclass.

LangGuard is a stateful, cyclic autonomous incident response agent built with **LangGraph**, **SQLite Checkpointers**, and **AST SQL Guardrails**. It investigates production billing discrepancies, self-heals broken queries, and enforces a deterministic **Human-in-the-Loop** breakpoint before issuing financial refunds.

---

## Architecture Highlights

1. **Type-Safe State Schema (`agent/state.py`)**:
   - Uses `TypedDict` and `Annotated[list, add_messages]` reducers so conversation history appends cleanly without overwriting prior state.
2. **AST SQL Firewall (`agent/tools.py`)**:
   - Parses every generated query into an Abstract Syntax Tree via `sqlparse` and blocks destructive `DROP`, `DELETE`, `TRUNCATE`, and `UPDATE` tokens before connecting to SQLite in read-only URI mode (`mode=ro`).
3. **Cyclic StateGraph & Conditional Routing (`agent/graph.py`)**:
   - Connects `triage -> query_db -> reconcile -> request_approval` with conditional self-healing loops.
4. **Durable SQLite Checkpointer & Breakpoints (`agent/graph.py`)**:
   - Persists every node transition to `state.db` via `SqliteSaver` and pauses execution deterministically using `interrupt_before=["request_approval"]`.

---

## Project Structure

```text
langguard-incident-copilot/
├── agent/
│   ├── __init__.py
│   ├── state.py      # Act 2: IncidentState TypedDict & add_messages reducer
│   ├── tools.py      # Act 3: @tool decorator & sqlparse AST firewall
│   ├── agent.py      # Act 4: ChatOpenAI(temperature=0.0) & bind_tools
│   ├── nodes.py      # Act 5: Pure Python state transformation nodes
│   └── graph.py      # Acts 5-7: StateGraph, conditional edges, SqliteSaver, compile()
├── run.py            # Act 8: End-to-end execution, AST test, breakpoint pause & resume
├── resume.py         # Act 8: Standalone CLI resume from SQLite checkpointer
└── requirements.txt
```

---

## Quickstart

### 1. Create a Virtual Environment & Install Dependencies

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Run the Full Incident Investigation & Breakpoint Demo

```bash
python run.py
```

### Expected Output

```text
=== 1. Testing AST SQL Firewall ===
[AST FIREWALL PASS] Blocked destructive query -> Security Alert: Destructive query DROP blocked.

=== 2. Running Incident Investigation (Thread INC-8820) ===
[triage] classified SEV-2 Billing Incident for customer_9021
[query_db] executing SELECT * FROM orders WHERE customer_id='customer_9021'...
[query_db] row count: 0
[reconcile] calculating credit delta: +$149.00 (orphaned Stripe charge detected)

[BREAKPOINT HALTED] Next node waiting in queue: ('request_approval',)
[CHECKPOINT STATE] order_status=AWAITING_APPROVAL, discrepancy=$149.00

=== 3. Simulating Operator Approval & Resuming from SQLite Checkpointer ===
[request_approval] operator decision: APPROVED. Issuing refund...
[execute_refund] Refund of $149.00 issued to customer_9021 (ch_3M9q82)

[FINAL STATE] order_status=RESOLVED, approval_granted=True, next=()
```

---

## License

MIT License. Built for **How Tech Runs** by **Dropout Developer**.
