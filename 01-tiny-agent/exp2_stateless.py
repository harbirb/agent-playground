from dotenv import load_dotenv
import anthropic
load_dotenv()

client = anthropic.Anthropic()


def ask(messages):
    response = client.messages.create(model="claude-haiku-5-5", max_tokens=1024, messages=messages)
    return next(b.text for b in response.content if b.type == "text")


# call 1
messages = [{"role": "user", "content": "My name is Harbir."}]
reply = ask(messages)
print("call 1:", reply)

# call 2: fresh messages list, call 1 is not included
print("call 2 (no history):", ask([{"role": "user", "content": "What's my name?"}]))

# call 3: history included
messages += [
    {"role": "assistant", "content": reply},
    {"role": "user", "content": "What's my name?"},
]
print("call 3 (with history):", ask(messages))
