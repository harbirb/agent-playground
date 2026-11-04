from dotenv import load_dotenv
import anthropic
load_dotenv()


client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What's the latest on the Mars rover?"}],
)
print(response)
