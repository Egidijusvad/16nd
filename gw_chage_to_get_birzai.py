from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API key from environment variable for security
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
client = OpenAI(api_key=api_key)

# Funkcija, kuri paima informaciją apie Biržus iš Vikipedijos
def get_birzai_info():
    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": "Biržai"
        }
    )
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    return page["extract"]

# Funkcijos aprašymas OpenAI modeliui
functions = [
    {
        "name": "get_birzai_info",
        "description": "Gauk trumpą santrauką apie Biržus iš Vikipedijos",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
    }
]

# Pirmasis naudotojo klausimas
messages = [
    {"role": "user", "content": "Papasakok apie Biržus"}
]

# Siunčiamas pirmasis užklausimas į OpenAI
response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages,
    functions=functions,
    function_call="auto",  # leidžiame modeliui pačiam nuspręsti, ar reikia iškviesti funkciją
)

response_message = response.choices[0].message

# Patikriname, ar modelis nori iškviesti funkciją
if response_message.function_call:
    function_name = response_message.function_call.name
    
    if function_name == "get_birzai_info":
        # Vykdome funkciją lokaliai
        function_response = get_birzai_info()

        # Antra žinutė su gauta funkcijos informacija
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                *messages,
                response_message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )

        # Atspausdiname galutinį atsakymą
        print(second_response.choices[0].message.content)
    else:
        print("Funkcija nerasta.")
else:
    print(response_message.content)
