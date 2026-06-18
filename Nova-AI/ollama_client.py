from ollama import Client

client = Client()

response = client.chat(
    model= "llama3:8b",
    messages=[
        {
            "role": "user", 
            "content": "Hello"
        }
    ]
)

print(response["message"]["content"])