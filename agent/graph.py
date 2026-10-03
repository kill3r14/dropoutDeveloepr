from langgraph.graph import StateGraph, START, END
from agent.state import IncidentState
from agent.nodes import triage, query_db, reconcile, request_approval

workflow = StateGraph(IncidentState)

# Register state transformation nodes
workflow.add_node("triage", triage)
workflow.add_node("query_db", query_db)
workflow.add_node("reconcile", reconcile)
workflow.add_node("request_approval", request_approval)

workflow.add_edge(START, "triage")
workflow.add_edge("triage", "query_db")

def route_after_sql(state: IncidentState) -> str:
    return "query_db" if state.get("raw_error") else "reconcile"
workflow.add_conditional_edges("query_db", route_after_sql)

workflow.add_edge("reconcile", "request_approval")
workflow.add_edge("request_approval", END)
from langgraph.checkpoint.sqlite import SqliteSaver, sqlite3
checkpointer = SqliteSaver(sqlite3.connect("state.db", check_same_thread=False))

app = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["request_approval"]
)
