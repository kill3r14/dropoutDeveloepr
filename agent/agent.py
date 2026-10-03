from langchain_openai import ChatOpenAI
from agent.tools import execute_safe_query, issue_stripe_refund

# Temperature 0.0: Strict determinism for production engineering
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

# Native tool binding transforms callables into OpenAI schemas
tools = [execute_safe_query, issue_stripe_refund]

llm_with_tools = llm.bind_tools(tools)
