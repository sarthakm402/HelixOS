import json 
import requests
ollama_url="http://localhost:11434/api/generate"
model_name="gemma3:4b"

def chat_with_llm(query):
    payload={
        "model":model_name,
        "prompt":query,
        "stream":True,
        "options":{"temperature":0}
    }

    response=requests.post(ollama_url,
    json=payload,stream=True)
    response.raise_for_status()
    for line in response.iter_lines():
        if line:
         chunk=json.loads(line)
        #  print(chunk)
         yield chunk["response"]