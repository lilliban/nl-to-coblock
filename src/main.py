import os
from src.knowledge_base.rule_generator import RuleGenerator
from src.connection.llm_factory import LLMFactory

# Insert API KEY
PROVIDER = "gemini"
API_KEY = os.getenv("GEMINI_API_KEY", ".......")
MODEL = "gemini-2.5-flash"

REQUIREMENTS = [
    # CR3
    "Check that the initial reporter (who stakes REP to validate an outcome) gets properly rewarded",
    # CR6
    "Allow anyone to create a market about any upcoming event. The end betting event date is not earlier than the market creation date.",
    # CR7
    "The creation bond, paid in REP, is returned to the market creator if  and only if the market’s designated reporter actually reports during the first 24 hours after the market’s event end time.",
]

if __name__ == "__main__":

    client = LLMFactory.create(PROVIDER, api_key=API_KEY, model=MODEL)
    generator = RuleGenerator(client)

    print(f"Provider: {client}")

    for fr in REQUIREMENTS:
        print(f"\nInput:  {fr}")
        print("Output:")
        risultato = generator.generate(fr)
        print(risultato)
        print("-" * 60)
