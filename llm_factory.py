from llm_client import GeminiClient, OpenAIClient, MockClient

class LLMFactory:

    @staticmethod
    def create(provider: str, api_key: str = "", model: str = ""):

        if provider == "gemini":
            return GeminiClient(api_key=api_key, model=model or "gemini-2.5-flash")

        elif provider == "openai":
            return OpenAIClient(api_key=api_key, model=model or "gpt-4o-mini")

        elif provider == "mock":
            return MockClient()

        else:
            raise ValueError(
                f"Provider '{provider}' non riconosciuto. "
                f"Usa: 'gemini', 'openai', o 'mock'."
            )