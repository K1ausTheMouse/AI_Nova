# the code that decides what to save

import json 
import ollama 
from AI_memory_system.context.prompt import CONTEXT_PROMPT


def process_context(user_input, response):

    prompt = f"""
You are Nova's context processor.

You are NOT a chatbot.

Your only job is to extract structured data.

Return ONLY valid JSON.

Do not explain.
Do not apologise.
Do not use markdown.
Do not write any text before or after the JSON.

The response MUST start with {{
The response MUST end with }}

Schema:

{{
  "summary": "string",
  "topic": "string",
  "mood": "string"
}}

User:
{user_input}

Nova:
{response}
"""
    


    result = ollama.chat(
        model="llama3:8b",
        messages=[{"role": "user", "content": prompt}]
    )

    print ("Reuslts: ", result)

    raw = result["message"]["content"].strip()

    print("raw ", raw)

    start = raw.find("{")
    end = raw.rfind("}") + 1

    if start == -1 or end == 0:
        print("Context processor did not return valid JSON:")
        print(raw)
        return {"summary": None, "topic": None, "mood": None}

    raw = raw[start:end]

    

    try:
        data = json.loads(raw)
        return{
            "summary": data.get("summary"),
            "topic": data.get("topic"),
            "mood": data.get("mood")
        }
    
    except json.JSONDecodeError:
        print("Context processor did not return valid JSON: ")
        print(raw)
        return {
            "summary": None,
            "topic": None,
            "mood": None
        }
















