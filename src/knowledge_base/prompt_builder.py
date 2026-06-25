from knowledge_base.coblock_syntax import COBLOCK_DOCS, COBLOCK_EXAMPLES

class PromptBuilder:

    def build(self, requirement: str, dapp_context: str = None) -> str:
        """
        Build the prompt for the LLM.

        Args:
            requirement:   The natural language compliance requirement.
            dapp_context:  Optional technical context for the target DApp
                           (function names, events, parameters, contract addresses).
                           If None → Mode 1 (prompt only).
                           If provided → Mode 2 (prompt + context).
        """
        prompt = (
            "You are an expert in CoBlock, a domain-specific language for writing "
            "compliance and security rules for blockchain systems. "
            "Your task is to translate a natural language requirement into a valid CoBlock rule.\n\n"
        )

        prompt += COBLOCK_DOCS + "\n\n"

        prompt += "EXAMPLES\n"
        for i, example in enumerate(COBLOCK_EXAMPLES, start=1):
            prompt += f"Example {i}:\n"
            prompt += f"Natural language: {example['nl']}\n"
            prompt += f"CoBlock rule:\n{example['rule']}\n\n"

        if dapp_context:
            prompt += (
                "APPLICATION CONTEXT\n"
                "The following describes the target application: its known function names, "
                "input parameters, emitted events, state variables, and contract addresses. "
                "Use this information to identify the correct technical identifiers "
                "when writing the CoBlock rule.\n\n"
            )
            prompt += dapp_context.strip() + "\n\n"

        prompt += f'Now translate the following requirement into a single CoBlock rule. Output only the rule, no explanations, no reasoning, no multiple alternatives.\n'
        prompt += f'Natural language: "{requirement}"\n'
        prompt += "CoBlock rule:"

        return prompt
