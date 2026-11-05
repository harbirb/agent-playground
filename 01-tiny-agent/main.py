import json
from dotenv import load_dotenv
import anthropic
load_dotenv()


client = anthropic.Anthropic()

def run_tool(name, input):
    if name == "add_numbers":
        return add(input["a"], input["b"])
    else:
        raise ValueError(f"Unknown tool: {name}")

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
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
        messages=messages,
    )

    print(f"raw response: {response}")

    while response.stop_reason == "tool_use":
        tool_use = next(block for block in response.content if block.type == "tool_use")
        print(f"Claude called {tool_use.name} with {json.dumps(tool_use.input)}")

        result = run_tool(tool_use.name, tool_use.input)
        messages += [
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [
                    {"type": "tool_result", "tool_use_id": tool_use.id, "content": json.dumps(result)}
                ],
            },
        ]

        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=1024,
            tools=tools,
            tool_choice={"type": "auto", "disable_parallel_tool_use": True},
            messages=messages,
        )

    # Claude uses the result to answer the original question.
    final_text = next(block for block in response.content if block.type == "text")
    print(final_text.text)

    print(f"raw response: {response}")


def add(a, b):
    return a + b

if __name__ == "__main__":
    main()