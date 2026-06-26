from src.knowledge_base.prompt_builder import PromptBuilder

class RuleGenerator:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.builder = PromptBuilder()
    def generate(self, user_sentence):
        # build the prompt and send it to the LLM
        return self.llm_client.generate(self.builder.build(user_sentence))
