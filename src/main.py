import json
import inspect

from ollama import chat

from tools.finance.getfees import total_fees_year  # noqa: F401
from tools.search.searchCustomer import getCustomerById
from tools.registry import TOOLS
from agent import Agent

print("Calling 2 Tools (function calling approach :")


def build_ollama_tools():
    ollama_tools = []

    for tool_name, tool_info in TOOLS.items():
        func = tool_info["function"]
        parameters = {}
        required = []

        for param_name, param in inspect.signature(func).parameters.items():
            if param_name == "self":
                continue

            if param.annotation in (int, float):
                ptype = "number"
            elif param.annotation is bool:
                ptype = "boolean"
            else:
                ptype = "string"

            parameters[param_name] = {
                "type": ptype,
                "description": f"Value for {param_name}"
            }
            required.append(param_name)

        ollama_tools.append({
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_info.get("description", ""),
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": required,
                },
            },
        })

    return ollama_tools



agent = Agent()

# Example: direct tool calls that already work
# print("Direct customer lookup:")
# print(getCustomerById("100009"))

# print("Agent tool call :")
# print(agent.total_fees_year())

# Ollama tool-calling section
messages = [
    {
        "role": "user",
        "content": "Use the tools to find patient 100009 and summarize the result."
    },
    {
        "role": "user",
        "content": "Use the tools to find total fees for year 2026 and summarize the result."
    }
]

ollama_tools = build_ollama_tools()

response = chat(
    model="llama3.1",
    messages=messages,
    tools=ollama_tools,
)

if response.message.tool_calls:
    for tool_call in response.message.tool_calls:
        tool_name = tool_call.function.name
        tool_args = tool_call.function.arguments or {}

        # Ensure the annual-fees call always includes the explicit year requested in
        # the user prompt even when the model omits it.
        if tool_name == "total_fees_year" and "year" not in tool_args:
            tool_args["year"] = 2026

        result = agent.orchestrator.execute_tool(tool_name, **tool_args)

        messages.append({
            "role": "tool",
            "tool_name": tool_name,
            "content": json.dumps(result),
        })

        response = chat(
            model="llama3.1",
            messages=messages,
            tools=ollama_tools,
        )
    print("Final response after tool calls: ....")
    print(response.message.content)
else:
    print(response.message.content)
