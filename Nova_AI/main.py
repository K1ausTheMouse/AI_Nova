from ollama_client import chat_with_nova
from prompt import SYSTEM_PROMPT
import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parent.parent / "AI_memory_system")
)

from MemoryDB_link import add_interaction

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
    })

    add_interaction(
        entity_id = None,
        type = "chat",
        user_input = user_input,
        response = response
    )
