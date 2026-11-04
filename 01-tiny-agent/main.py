from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

import anthropic

client = anthropic.Anthropic(api_key=api_key)

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What's the latest on the Mars rover?"}],
)
print(response)
