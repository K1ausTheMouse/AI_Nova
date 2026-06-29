# the code that decides what to save

import json 
import ollama 
from AI_memory_system.context.prompt import CONTEXT_PROMPT

def process_context(user_input, response):
    prompt = f"""
    
Summarise this interaction in one short sentence.

> 
{user_input}

Nova:
{response}

Return only the sentence.
 """
    
    result = ollama.chat(
        model="llama3:8b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )


    summary = result["message"]["content"].strip()
    return summary


























"""
    raw = result["message"]["content"]

    try:
        data = json.loads(raw)
        print(data)
        return data
    
    except json.JSONDecodeError:
        print("Context processor did not return valid JSON: ")
        print(raw)
        return None

"""