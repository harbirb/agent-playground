import json

from dotenv import load_dotenv, main
import anthropic
load_dotenv()


client = anthropic.Anthropic()


def main():
    tools = [
        {
            "name": "add_numbers",
            "description": "Add two numbers.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number.",
                    }
                },
                "required": ["a", "b"],
            },
        }
    ]
    messages = [{"role": "user", "content": "What is 1234 plus 5678?"}]


    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    print(f"raw response: {response}")

    tool_use = next(block for block in response.content if block.type == "tool_use")
    print(f"Claude called {tool_use.name} with {json.dumps(tool_use.input)}")

    sum = add(tool_use.input["a"], tool_use.input["b"])
    messages += [
        {"role": "assistant", "content": response.content},
        {
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": tool_use.id, "content": str(sum) }
            ],
        },
    ]

    followup = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    # Claude uses the result to answer the original question.
    final_text = next(block for block in followup.content if block.type == "text")
    print(final_text.text)

    print(f"raw response: {followup}")


def add(a, b):
    return a + b

if __name__ == "__main__":
    main()