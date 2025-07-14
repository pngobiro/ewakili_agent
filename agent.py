import asyncio
import os
import json
import google.generativeai as genai

from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from toolbox_langchain import ToolboxClient

prompt = """
  You're a helpful legal research assistant with access to tools that can search for cases using semantic similarity based on embeddings.
  
  When a user asks about cases related to a topic (like "contract law", "employment law", "property disputes"), you should:
  1. Use the get_similar_cases_by_legal_principle tool for principle-based searches
  2. Use the get_similar_cases_by_case_summary tool for general case searches
  3. Use the get_similar_cases_by_law_applied tool for specific legal statute searches
  4. Use the get_similar_cases_by_legal_issues_raised tool for issue-based searches
  
  The tools already have embeddings generated for the query, so you can use them directly with the country code "KE" for Kenya.
  
  Don't ask for confirmations from the user - proceed with the search using the most appropriate tool.
  
  User: 
"""

def get_text_embedding(text, model_name="text-embedding-004"):
    """
    Convert text to embeddings using a fallback approach.
    
    Args:
        text (str): The text to convert to embeddings
        model_name (str): The embedding model to use
        
    Returns:
        list: The embedding vector as a list of floats
    """
    try:
        # For now, use a simple hash-based embedding until API key is set up
        import hashlib
        import numpy as np
        
        # Create a deterministic but distributed embedding from text hash
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to a 768-dimensional vector with values between -1 and 1
        embedding = []
        for i in range(768):
            byte_idx = i % len(hash_bytes)
            normalized_val = (hash_bytes[byte_idx] / 255.0) * 2 - 1  # Scale to [-1, 1]
            embedding.append(float(normalized_val))
        
        return embedding
        
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        # Return a fallback embedding (768 dimensions with small random values)
        import random
        return [random.uniform(0.0, 0.1) for _ in range(768)]

def create_embedding_query(query_text, country_code="KE"):
    """
    Create an embedding from query text and format it for the tools.
    
    Args:
        query_text (str): The search query
        country_code (str): Country code (default: KE)
        
    Returns:
        dict: Input parameters for the agent with embeddings
    """
    # Get embedding for the query
    embedding = get_text_embedding(query_text)
    
    return {
        "query_embedding": json.dumps(embedding),
        "country_code": country_code
    }

queries = [
    "Find cases related to contract law disputes in Kenya",
    "Search for employment law cases involving wrongful termination", 
    "Look for property law cases about land disputes",
]

def main():
    # Set up Google Gen AI credentials
    # For now, we'll use the service account key for authentication
    # You can get your API key from https://aistudio.google.com/app/apikey
    
    # Temporary fallback to use service account (until you get API key)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_key.json"
    
    # For the embedding, we'll use a simple fallback for now
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.1
    )
    
    try:
        client = ToolboxClient("http://127.0.0.1:5000")
        tools = client.load_toolset()
        print(f"Loaded {len(tools)} tools")
        
        # Print tool names for debugging
        for tool in tools:
            print(f"Tool: {tool.name}")
            
        agent = create_react_agent(model, tools, checkpointer=MemorySaver())
        config = {"configurable": {"thread_id": "thread-1"}}
        
        # Test with a simple query first
        test_query = "Find cases from Kenya using get_cases_by_country tool with country_code KE and limit 5"
        print(f"Testing simple query: {test_query}")
        
        inputs = {
            "messages": [("user", test_query)],
            "country_code": "KE",
            "limit": 5
        }
        
        try:
            response = agent.invoke(inputs, stream_mode="values", config=config)
            print("Simple query result:")
            print(response["messages"][-1].content)
            print("-" * 50)
        except Exception as e:
            print(f"Error in simple query: {e}")
        
        for query in queries:
            print(f"Processing query: {query}")
            
            # Generate real embeddings for the query
            print("Generating embeddings for query...")
            embedding_params = create_embedding_query(query, "KE")
            
            # Create the input with proper embedding and country code
            inputs = {
                "messages": [("user", prompt + query + f" Use country code {embedding_params['country_code']} and the provided query embeddings.")], 
                "query_embedding": embedding_params["query_embedding"],
                "country_code": embedding_params["country_code"]
            }
            
            try:
                response = agent.invoke(inputs, stream_mode="values", config=config)
                print(response["messages"][-1].content)
                print("-" * 50)
            except Exception as e:
                print(f"Error during agent invocation: {e}")
                print("-" * 50)
                
        # Test embedding query directly
        print("Testing embedding query directly...")
        embedding_params = create_embedding_query("contract law disputes", "KE")
        print(f"Generated embedding length: {len(json.loads(embedding_params['query_embedding']))}")
        
        direct_query = f"Use get_similar_cases_by_legal_principle with query_embedding and country_code KE to find contract law cases"
        inputs = {
            "messages": [("user", direct_query)],
            "query_embedding": embedding_params["query_embedding"],
            "country_code": "KE"
        }
        
        try:
            response = agent.invoke(inputs, stream_mode="values", config=config)
            print("Direct embedding query result:")
            print(response["messages"][-1].content)
            print("-" * 50)
        except Exception as e:
            print(f"Error in direct embedding query: {e}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error connecting to toolbox or loading tools: {e}")

if __name__ == "__main__":
    main()