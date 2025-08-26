
# OLLAMA_DEBUG=1 /Applications/Ollama.app/Contents/Resources/ollama serve

# test_rag_ollama.py
import requests
import json

def test_rag_with_ollama(query, context):
    """
    Test RAG with Ollama locally
    """
    prompt = f"""Based on the following context, answer the question:

Context: {context}

Question: {query}

Answer:"""
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:1b",  # Change to your preferred model
            "prompt": prompt,
            "stream": False
        }
    )
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.text}"

# Example usage
if __name__ == "__main__":
    context = "The company was founded in 2015 and specializes in AI technology. It has offices in San Francisco and New York."
    query = "When was the company founded?"
    
    answer = test_rag_with_ollama(query, context)
    print(f"Question: {query}")
    print(f"Answer: {answer}")