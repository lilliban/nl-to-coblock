from src.knowledge_base.prompt_builder import PromptBuilder

class RuleGenerator:

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.builder = PromptBuilder()

    def generate(self, frase_utente):
        #build prompt
        prompt = self.builder.build(frase_utente)
        #send to LLM
        risposta = self.llm_client.generate(prompt)

        return risposta


