### notes

#### When you give the model a tool, what exactly do you send? (A name, a description, and what else?)

- You send the model the name, description and the shcema of the tool's input.

#### Does the model run your add function? If not, who does?

- the model does not run your function. You run it in your application since it is considered a client tool ( a user defined tool )

#### What does the model’s response look like when it wants to use a tool, and how is that different from a normal text answer?

- when it wants to use a tool, it includes a "stop_reason" of tool_use and a tool_use block as part of the response. the tool_use block has fields for the id, name, and input being passed to the tool. A normal text answer has a stop_reason of just 'end_turn'.

#### After you run the function, what do you send back, and why does the model need it?

- after running the fn, you send back the tool_result (the answer) so the model can use with it in the next message. As part of this, you must reply back with a content block of type "tool_result", role of user, and include the tool_use_id that matches the id from the first response. And the content field for what the actual tool use result was. The api is stateless. Thus, you must also remember to send the thread of messages back to the model so it knows what the context was. So you send the original message, plus the response, plus the tool result back.

```messages += [
    {"role": "assistant", "content": response.content},
    {
        "role": "user",
        "content": [
            {"type": "tool_result", "tool_use_id": tool_use.id, "content": weather}
        ],
    },
]
```

#### Plain tool call

- I called the api with no tools provided. It returns a content block of type text containing the answer and the stop reason of end_turn.
- Content returns a thinking block and a text block. The answer isn't always in content[0], must find a block by its type.
- The max_tokens arg will have to cover the tokens required for both the thinking_tokens and the output_tokens.

#### call with tools provided:

- called api with add_numbers tool provided. It returns a content block of type "tool_use" that gives us the inputs defined by the tool. We call the tool with the inputs and get back the output. We then send back a content block of type "tool_result" and provide the tool_use_id from the first response and the content is the tool result. We append that to the messages list and send it back to the model since its stateless. Then it responded with a content block of type "text" containing the answer and the stop reason of end_turn.

#### Agentic loop:

- Real calls often have several tool calls. We can use a while loop that keeps running tools and feeding results back until stop_reason is no longer "tool_use". While the api keeps responding with stop_reason == "tool_use", that means we have more tools to use. We keep appending to the messages array on each request to include prior context.

If we askthe model for : (3 + 4) \* 5
It will return the following responses:
one response to add 3 and 4, one to multiply the result of that by 5, and then the last one will return the final answer.

#### Parallel tool use:

- when the model returns several tool use blocks, you owe it one tool result for each. Parallel tool use is enabled by default. Set "disable_parallel_tool_use": True in tool_choice to turn it off.
