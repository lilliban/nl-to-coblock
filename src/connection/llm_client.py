from abc import ABC, abstractmethod

class LLMClient(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Invia un prompt all'LLM e restituisce la risposta come stringa."""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class GeminiClient(LLMClient):

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model = model
        from google import genai
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text.strip()


class OpenAIClient(LLMClient):
    def generate(self, prompt: str) -> str:
        pass

class MockClient(LLMClient):
    def generate(self, prompt: str) -> str:
        pass