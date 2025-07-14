import asyncio
import os
import json
import vertexai

from langgraph.prebuilt import create_react_agent
from langchain_google_vertexai import ChatVertexAI
from langgraph.checkpoint.memory import MemorySaver
from toolbox_langchain import ToolboxClient

prompt = """
  You're a helpful legal research assistant. 
  You can use the provided tools to search for cases.
  Don't ask for confirmations from the user.
  User: 
"""

queries = [
    "Find 10 cases in Kenya related to contract law. Use the get_cases_by_country tool with country code KE and limit to 10 cases.",
]

def main():
    # Set up Google Cloud credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_key.json"
    
    vertexai.init(project="gen-lang-client-0552746813")
    model = ChatVertexAI(model_name="gemini-2.5-pro")
    
    try:
        client = ToolboxClient("http://127.0.0.1:5000")
        tools = client.load_toolset()
        print(f"Loaded {len(tools)} tools")
        
        # Print tool names for debugging
        for tool in tools:
            print(f"Tool: {tool.name}")
            
        agent = create_react_agent(model, tools, checkpointer=MemorySaver())
        config = {"configurable": {"thread_id": "thread-1"}}
        
        for query in queries:
            print(f"Processing query: {query}")
            # This is a placeholder for getting a real embedding.
            # In a real application, you would use a model to get the embedding for the query.
            embedding = [0.1] * 768
            inputs = {"messages": [("user", prompt + query)], "query_embedding": json.dumps(embedding)}
            
            try:
                response = agent.invoke(inputs, stream_mode="values", config=config)
                print(response["messages"][-1].content)
            except Exception as e:
                print(f"Error during agent invocation: {e}")
                
    except Exception as e:
        print(f"Error connecting to toolbox or loading tools: {e}")

if __name__ == "__main__":
    main()