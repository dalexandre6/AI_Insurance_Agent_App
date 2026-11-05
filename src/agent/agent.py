from agent.orchestrator import Orchestrator


class Agent:

    def __init__(self):
        self.orchestrator = Orchestrator()

    #def run(self):
    def total_fees_year(self):
        # total_fees_year takes no arguments
        result = self.orchestrator.execute_tool("total_fees_year")
        return result

    def get_customer(self, customer_id):
        return self.orchestrator.execute_tool("getCustomerById", customer_id)

    #Send prompts to LLM :

    