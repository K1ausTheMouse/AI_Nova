# novas tool box 😋

import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parent.parent / "AI_memory_system")
)

import MemoryDB_link 



def find_relevant_context(user_input):

    recent = MemoryDB_link.get_recent_interactions(limit = 10)

    context = "\n".join(
        f"User:{item['input']}\n Nova: {item['response']}"
        for item in reversed(recent)
    )

    return context




"""
remember_fact()
search_entities()
compress_old_chats()
"""