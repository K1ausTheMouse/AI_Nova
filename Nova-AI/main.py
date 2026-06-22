from ollama_client import chat_with_nova
from prompt import SYSTEM_PROMPT

messages = []

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


while True:

    user_input = input("> ")

    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = chat_with_nova(messages)

    print(f"\n Nova: {response}\n")

    messages.append({
        "role": "assistant",
        "content": response
    }

)