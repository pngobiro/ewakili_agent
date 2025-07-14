#!/usr/bin/env python3

import json
from toolbox_langchain import ToolboxClient

def test_toolbox_direct():
    """Test the toolbox client directly"""
    
    try:
        client = ToolboxClient("http://127.0.0.1:5000")
        tools = client.load_toolset()
        
        print(f"Loaded {len(tools)} tools")
        
        # Find the legal principle tool
        legal_principle_tool = None
        for tool in tools:
            if "legal_principle" in tool.name:
                legal_principle_tool = tool
                break
        
        if legal_principle_tool is None:
            print("Could not find legal principle tool")
            return
            
        print(f"Found tool: {legal_principle_tool.name}")
        print(f"Tool description: {legal_principle_tool.description}")
        
        # Create test parameters
        test_embedding = [0.1] * 768
        embedding_json = json.dumps(test_embedding)
        
        print(f"Testing with embedding length: {len(test_embedding)}")
        
        # Try to invoke the tool directly
        try:
            result = legal_principle_tool.invoke({
                "query_embedding": embedding_json,
                "country_code": "KE"
            })
            
            print("Tool invocation successful!")
            print(f"Result type: {type(result)}")
            print(f"Result: {str(result)[:500]}...")
            
        except Exception as e:
            print(f"Error invoking tool: {e}")
            print(f"Error type: {type(e)}")
            
    except Exception as e:
        print(f"Error with toolbox client: {e}")

if __name__ == "__main__":
    test_toolbox_direct()
