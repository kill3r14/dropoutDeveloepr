from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages

class IncidentState(TypedDict):
    incident_id: str
    customer_id: str
    messages: Annotated[list, add_messages]
    discrepancy_amount: float
    order_status: Optional[str]
    raw_error: Optional[str]
    approval_granted: Optional[bool]
