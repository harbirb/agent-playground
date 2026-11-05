import json
from dotenv import load_dotenv
import anthropic
load_dotenv()


client = anthropic.Anthropic()
MAX_PASSES = 10

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b


tool_functions = {
    "add_numbers": add,
    "multiply_numbers": multiply,
}

def run_tool(name, input):
    if name in tool_functions:
        return tool_functions[name](input["a"], input["b"])
    else:
        raise ValueError(f"Unknown tool: {name}")

def main():
    tool_definitions = [
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
        },
        {
            "name": "multiply_numbers",
            "description": "Multiply two numbers.",
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
    messages = [{"role": "user", "content": "What is (1234 + 5678) * 23 + (123*125+134)"}]


    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1024,
        tools=tool_definitions,
        tool_choice={"type": "auto", "disable_parallel_tool_use": False},
        messages=messages,
    )

    pass_number = 1
    while response.stop_reason == "tool_use":
        if pass_number > MAX_PASSES:
            print(f"Stopped after reaching the maximum of {MAX_PASSES} tool-use passes.")
            return

        tool_uses = [block for block in response.content if block.type == "tool_use"]
        tool_results = []
        for tool_use in tool_uses:
            print(f"Claude called {tool_use.name} with {json.dumps(tool_use.input)}")
            try:
                result = run_tool(tool_use.name, tool_use.input)
            except Exception as error:
                # a bad tool call should not fail the loop
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": str(error),
                        "is_error": True,
                    }
                )
            else:
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": json.dumps(result),
                    }
                )

        messages += [
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": tool_results},
        ]

        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=1024,
            tools=tool_definitions,
            tool_choice={"type": "auto", "disable_parallel_tool_use": False},
            messages=messages,
        )
        pass_number += 1

    # Claude uses the result to answer the original question.
    if response.stop_reason == "end_turn":
        final_text = next(block for block in response.content if block.type == "text")
        print(final_text.text)
    else:
        print(f"Stopped after {pass_number} passes with stop reason: {response.stop_reason}")
        print(response.content)

if __name__ == "__main__":
    main()