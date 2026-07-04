import json 
import requests
from core.config import OLLAMA_URL,MODEL_NAME,TEMPERATURE
ollama_url=OLLAMA_URL
model_name=MODEL_NAME

def chat_with_llm(query):
    payload = {
     "model": model_name,
     "prompt": query,
     "stream": True,
     "keep_alive": "30m",
     "options": {
        "temperature": TEMPERATURE,
        "num_ctx": 2048
     }
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
   prompt = f"""
You are a senior software architect and repository analyst.

Your task is to understand a code repository from its documentation,
text files, and extracted code metadata.

Repository Information
======================

README FILES:
{repo_info['readme_snapshot']}

TEXT FILES:
{repo_info['txt_snapshot']}

CODE METADATA:
{repo_info['code_files']}

Analysis Instructions
=====================

Analyze the repository in the following order:

1. Determine the primary purpose of the project.
2. Use code metadata as the source of truth.
3. Use README files to understand stated goals and intent.
4. Identify major components and responsibilities.
5. Identify likely execution flow.
6. Identify probable entry points.
7. Identify the most important files/modules.
8. Infer how the system is expected to be used.
9. Mention inconsistencies between README claims and code structure if any exist.

Important Rules
===============

- Prefer code structure over README descriptions when they disagree.
- Do not invent functionality that is not supported by the repository data.
- If information is uncertain, explicitly state that it is inferred.
- Focus on architecture and responsibilities rather than implementation details.
- Keep summaries concise and factual.

Return ONLY valid JSON.

JSON Schema
===========

{{
  "project_name": "",
  "intent_guess": "",
  "project_type": "",
  "entry_points": [],
  "architecture_summary": "",
  "main_components": [
    {{
      "name": "",
      "purpose": ""
    }}
  ],
  "execution_flow": "",
  "key_files": [],
  "core_directories": [],
  "readme_summary": "",
  "quick_start": "",
  "confidence": "",
  "notes": []
}}

Field Guidance
==============

project_name:
    Repository or project name.

intent_guess:
    One sentence describing the primary goal.

project_type:
    Examples:
    - CLI Application
    - Web Application
    - AI Agent System
    - Machine Learning Project
    - Library
    - Data Pipeline
    - Automation Platform

architecture_summary:
    High-level explanation of how components interact.

main_components:
    Major subsystems and their responsibilities.

execution_flow:
    Describe the likely runtime flow from user input to output.

key_files:
    Most important files for understanding the project.

core_directories:
    Most important directories.

quick_start:
    Which file a developer should open first.

confidence:
    High, Medium, or Low.

notes:
    Additional observations or uncertainties.
"""
   payload = {
    "model": model_name,
    "prompt": prompt,
    "stream": False,
    "keep_alive": "30m",
    "options": {
        "temperature": TEMPERATURE,
        "num_ctx": 2048
    }
}
   response=requests.post(ollama_url,
   json=payload)
   response.raise_for_status()
   summary=response.json()
   return summary['response']

   