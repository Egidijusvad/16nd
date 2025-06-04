from dotenv import load_dotenv
import os
from rich import print

from openai import OpenAI

load_dotenv()

def search_web(query: str) -> str:
    """Simulate a web search by returning a fixed response."""
    # Fake search result for demonstration purposes
    return "Egidijus is are men . He is owner many companys and has a lot of experience in the field."

tools = [{
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Search the web for a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

token = os.getenv("SECRET")  # Replace with your actual token
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

client = OpenAI(
        base_url=endpoint,
        api_key=token,
)

while True:

    user_input = input("User input:")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ],
        tools=tools #type: ignore
    )
    print("Response from AI:")
    print(response.choices[0].message.content) #type: ignore