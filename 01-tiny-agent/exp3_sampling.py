from dotenv import load_dotenv
import anthropic
load_dotenv()

# Latest client does not support the temperatures parameter so we have to use the default_headers and extra_body to pass it in.
client = anthropic.Anthropic(
    default_headers={"anthropic-version": "2023-06-01"}
)

prompt = "One sentence - the cat sat..."


def ask(temperature):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        # temperature=temperature,
        extra_body={"temperature": temperature},
        messages=[{"role": "user", "content": prompt}],
    )
    return next(b.text for b in response.content if b.type == "text")


for temperature in (1.0, 0.0):
    print(f"--- temperature {temperature} ---")
    for _ in range(5):
        print(ask(temperature))
