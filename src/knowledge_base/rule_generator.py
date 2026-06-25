from knowledge_base.prompt_builder import PromptBuilder

class RuleGenerator:

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.builder = PromptBuilder()

    def generate(self, requirement: str, dapp_context: str = None) -> str:
        """
        Generate a CoBlock rule from a natural language requirement.

        Args:
            requirement:   Natural language compliance requirement.
            dapp_context:  Optional DApp technical context (Mode 2).
                           If None, runs in Mode 1 (prompt only).
        """
        prompt = self.builder.build(requirement, dapp_context=dapp_context)
        return self.llm_client.generate(prompt)
