#!/usr/bin/env python3

import json
import requests

def test_toolbox_embedding():
    """Test the toolbox server directly with embedding parameters"""
    
    # Create a test embedding (768 dimensions)
    test_embedding = [0.1] * 768
    embedding_json = json.dumps(test_embedding)
    
    print(f"Testing embedding with length: {len(test_embedding)}")
    
    # Test the toolbox endpoint directly
    url = "http://127.0.0.1:5000/api/tools/get_similar_cases_by_legal_principle"
    
    payload = {
        "query_embedding": embedding_json,
        "country_code": "KE"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                print(f"Found {len(data['results'])} results")
                print(f"First result: {data['results'][0]}")
            else:
                print("No results found")
        else:
            print("Error response from toolbox")
            
    except Exception as e:
        print(f"Error calling toolbox: {e}")

if __name__ == "__main__":
    test_toolbox_embedding()
