# the code that decides what to save

import json 
import ollama 
from AI_memory_system.context.prompt import CONTEXT_PROMPT

def generate_summary(user_input, response):
    prompt = f"""
    
Summarise this interaction in one short sentence.

User:
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





def generate_topic(user_input, response):
    prompt = f"""
    
Determine the primary topic of this interaction.

Rules:
- Return only the topic.
- Use 1 to 5 words.
- Be specific when possible.
- Do not explain.

User:
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


    topic = result["message"]["content"].strip()
    return topic
























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