import json
from dotenv import load_dotenv
import anthropic
load_dotenv()

client = anthropic.Anthropic()

tool_functions = {
    "add_numbers": lambda a, b: a + b,
    "multiply_numbers": lambda a, b: a * b,
}

number_schema = {
    "type": "object",
    "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
    "required": ["a", "b"],
}

tools = [
    {"name": "add_numbers", "description": "Add two numbers.", "input_schema": number_schema},
    {"name": "multiply_numbers", "description": "Multiply two numbers.", "input_schema": number_schema},
]


def run(system=anthropic.NOT_GIVEN):
    messages = [{"role": "user", "content": "What is (1234 + 5678) * 23 + (123*125+134)"}]
    while True:
        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=1024,
            system=system,
            tools=tools,
            messages=messages,
        )
        print(response.usage.input_tokens, response.usage.output_tokens)

        if response.stop_reason != "tool_use":
            break

        results = []
        for block in response.content:
            if block.type == "tool_use":
                result = tool_functions[block.name](**block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)})

        messages += [
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": results},
        ]

    return next(b.text for b in response.content if b.type == "text")


print("--- no system prompt ---")
print(run())

print("--- system: Answer with only the number. ---")
print(run(system="Answer with only the number."))
