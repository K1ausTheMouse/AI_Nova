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



def processor_entities(user_input, response):

    prompt = f"""
You are Nova's entity extractor.

Return ONLY valid JSON.

Extract entity updates from the conversation.

Rules:
- If no entity information is found, return action "ignore".
- Use action "update" if the entity already seems known.
- Use action "add" only for a new person/object/system.
- Unknown fields must be null.
 - If the user refers to Klaus,me, my, I, or user, update Klaus Mouse. Do not add a new entity.

Return this JSON shape:
{{
  "action": "ignore/add/update",
  "match_name": null,
  "name": null,
  "surname": null,
  "age": null,
  "type": null,
  "description": null,
  "aliases": []
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
        return {
            "action": data.get("action", "ignore"),
            "match_name": data.get("match_name"),
            "name": data.get("name"),
            "surname": data.get("surname"),
            "age": data.get("age"),
            "type": data.get("type"),
            "description": data.get("description"),
            "aliases": data.get("aliases", [])
        }

    raw = raw[start:end]

    

    try:
        data = json.loads(raw)
        return {
            "action": data.get("action", "ignore"),
            "match_name": data.get("match_name"),
            "name": data.get("name"),
            "surname": data.get("surname"),
            "age": data.get("age"),
            "type": data.get("type"),
            "description": data.get("description"),
            "aliases": data.get("aliases", [])
        }
            
        
    
    except json.JSONDecodeError:
        print("Context processor did not return valid JSON: ")
        print(raw)
        return {
            "action": None,
            "match_name": None,
            "name": None,
            "surname": None,
            "type": None,
            "description": None,
            "aliases": None
        }












