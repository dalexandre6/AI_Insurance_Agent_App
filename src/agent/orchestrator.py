from tools.registry import TOOLS
#Acts like the brain (when there is no MCP):
#The orchestrator knows: 1.Find tools. 2.Invoke tools. 3.Return results


class Orchestrator:

    def execute_tool(self, tool_name, *args, **kwargs):

        if tool_name not in TOOLS:
            raise Exception(
                f"Tool '{tool_name}' not found."
            )

        tool = TOOLS[tool_name]["function"]

        return tool(*args, **kwargs)

    def list_tools(self):

        return list(TOOLS.keys())