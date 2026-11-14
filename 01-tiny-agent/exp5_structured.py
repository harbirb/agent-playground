import json
from dotenv import load_dotenv
from pydantic import BaseModel
import anthropic
load_dotenv()

client = anthropic.Anthropic()

RUNS = 10
prompt = "Extract name and age from: Priya Natarajan turned 34 last week and is starting a new job on Monday."


class Person(BaseModel):
    name: str
    age: int


# Part A: ask for JSON in the prompt, then json.loads it
failures = 0
for i in range(RUNS):
    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    output = next(b.text for b in response.content if b.type == "text")
    try:
        json.loads(output)
    except json.JSONDecodeError:
        failures += 1
        print(f"[A] run {i + 1} failed to parse:\n{output}\n")
print(f"Part A (prompt only): {failures}/{RUNS} parse failures\n")

# Part B: native structured outputs via messages.parse
failures = 0
for i in range(RUNS):
    try:
        response = client.messages.parse(
            model="claude-haiku-5-5",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
            output_format=Person,
        )
        print(f"[B] run {i + 1}: {response.parsed_output}")
    except Exception as error:
        failures += 1
        print(f"[B] run {i + 1} failed: {error}")
print(f"Part B (structured outputs): {failures}/{RUNS} failures")
