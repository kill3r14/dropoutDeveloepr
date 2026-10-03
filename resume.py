from agent.graph import app

config = {"configurable": {"thread_id": "INC-8820"}}

print("Resuming paused thread INC-8820 from SQLite checkpointer...")
result = app.invoke(None, config=config)
final_snapshot = app.get_state(config)
print(f"Status: {final_snapshot.values.get('order_status')} | Approval Granted: {final_snapshot.values.get('approval_granted')}")
