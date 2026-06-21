import os
import google.genai as genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

print("Available Models:")
for m in client.models.list():
    print(f"- {m.name}")
