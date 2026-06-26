from src.knowledge_base.coblock_syntax import COBLOCK_DOCS, COBLOCK_EXAMPLES

class PromptBuilder:
    def build (self, user_sentence):
        prompt = "You are an expert in CoBlock, a domain-specific language for writing compliance and security rules for blockchain systems. Your task is to translate a natural language sentence into a valid CoBlock rule.\n\n"
        prompt += COBLOCK_DOCS + "\n\n"
        prompt += "EXAMPLES \n"
        for i, example in enumerate(COBLOCK_EXAMPLES, start=1):
            prompt += f"Example {i}:\n"
            prompt += f"Natural language: {example['nl']}\n"
            prompt += f"CoBlock rule: {example['rule']}\n\n"
        prompt += f"Natural language: \"{user_sentence}\"\n"
        prompt += "CoBlock rule:"
        return prompt
