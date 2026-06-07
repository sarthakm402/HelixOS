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
def create_summary(repo_info):
   prompt=f"""
You are an expert repository analyzer.

README:
{repo_info['readme_snapshot']}

TEXT FILES:
{repo_info['txt_snapshot']}

CODE FILES:
{repo_info['code_files']}

Return JSON:

{{
  "project_name": "",
  "intent_guess": "",
  "entry_points": [],
  "structure": {{
      "core_dirs": [],
      "key_files": []
  }},
  "readme_summary": "",
  "quick_start": ""
}}"""
   payload={
      "model":model_name,
      "prompt":prompt,
      "stream":False
   }
   response=requests.post(ollama_url,
   json=payload)
   response.raise_for_status()
   summary=response.json()
   return summary['response']
   
   