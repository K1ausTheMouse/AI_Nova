from ollama import Client

client = Client()

def chat_with_nova(messages):

    response = client.chat(
        model = "llama3:8b",
        messages = messages
    )

    return (response["message"]["content"])