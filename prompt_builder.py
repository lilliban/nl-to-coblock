from coblock_syntax import COBLOCK_DOCS, COBLOCK_EXAMPLES

class PromptBuilder:

    def build (self, frase_utente):

        prompt = "You are an expert in CoBlock, a domain-specific language for writing compliance and security rules for blockchain systems. Your task is to translate a natural language sentence into a valid CoBlock rule.\n\n"
        prompt += COBLOCK_DOCS + "\n\n"

        prompt += "EXAMPLES \n"
        for i, esempio in enumerate(COBLOCK_EXAMPLES, start=1):
            prompt += f"Example {i}:\n"
            prompt += f"Natural language: {esempio['nl']}\n"
            prompt += f"CoBlock rule: {esempio['rule']}\n\n"

        prompt += f"Natural language: \"{frase_utente}\"\n"
        #convezione del prompt enginering, perchè permette di capire agli LLM dove scrivere la risposta
        prompt += "CoBlock rule:"


        return prompt



if __name__ == "__main__":
    builder = PromptBuilder()
    risultato = builder.build("The initial reporter must get properly rewarded")
    print(risultato)