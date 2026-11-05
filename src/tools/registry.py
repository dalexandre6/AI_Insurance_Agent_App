TOOLS = {}


def register_tool(name, description):

    def decorator(func):
        TOOLS[name] = {
            "function": func,
            "description": description,
        }

        return func

    return decorator
