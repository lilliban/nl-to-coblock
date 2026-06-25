import os
import time
from knowledge_base.rule_generator import RuleGenerator
from connection.llm_factory import LLMFactory
from knowledge_base.dapp_context import AUGUR_CONTEXT, PANCAKESWAP_CONTEXT, BEANSTALK_CONTEXT


PROVIDER = "gemini"
API_KEY  = os.getenv("GEMINI_API_KEY", "......")
MODEL    = "gemini-2.5-flash"


# 0 = Augur CR3
# 1 = Augur CR6
# 2 = Augur CR7
# 3 = PancakeSwap R6
# 4 = PancakeSwap R7
# 5 = Beanstalk

TEST_CASES = [

    # 0 ── Augur CR3
    (
        "Augur CR3",
        "Check that the initial reporter (who stakes REP to validate an outcome) gets properly rewarded.",
        "redeemInitRepTX(function is RedeemAsInitialReporter)\nnef > 0 blocks\nfinalizeTX(function is FinalizeMarket)",
        AUGUR_CONTEXT,
    ),

    # 1 ── Augur CR6
    (
        "Augur CR6",
        "Allow anyone to create a market about any upcoming event. "
        "The end betting event date is not earlier than the market creation date.",
        "createTX(function is CreateMarket\n    is passed endTime (< createTX.timestamp)) nocc",
        AUGUR_CONTEXT,
    ),

    # 2 ── Augur CR7
    (
        "Augur CR7",
        "The creation bond, paid in REP, is returned to the market creator if and only if "
        "the market's designated reporter actually reports during the first 24 hours after "
        "the market's event end time.",
        (
            "reportTX(sender is createTX.designatedRepoter\n"
            "    function is SubmitInitialReport\n"
            "    is emitted Transfer(is contained to (= createTX.sender)\n"
            "    is contained value (= createTX.BOND)))\n"
            "ef < (createTX.endTime - createTX.timestamp) + 86400 seconds\n"
            "createTX(contract is 0x7677 function is CreateMarket)"
        ),
        AUGUR_CONTEXT,
    ),

    # 3 ── PancakeSwap R6
    (
        "PancakeSwap R6",
        "A contract ownership transfer is only valid if the new owner is not null, "
        "the owner state variable is correctly updated, and the OwnershipTransferred "
        "event is emitted with the correct previous owner address.",
        (
            "transOwnTX(function is transferOwnership\n"
            "    is passed newOwner(!= nil)\n"
            "    is updated _owner(!= transOwnTX.inputs.newOwner)\n"
            "    is emitted OwnershipTransferred(is contained previousOwner(!= transOwnTX.sender))) nocc"
        ),
        PANCAKESWAP_CONTEXT,
    ),

    # 4 ── PancakeSwap R7
    (
        "PancakeSwap R7",
        "Every cross-chain token transfer must make the required call to the LayerZero "
        "protocol to handle the communication. Transfers that bypass LayerZero are invalid.",
        (
            "transTokTX(function is sendFrom\n"
            "    is called STATICCALL(contract is not 00000000000000000000000066a71dcef29a0ffbdbe3c6a460a3b5bc225cd675)) nocc"
        ),
        PANCAKESWAP_CONTEXT,
    ),

    # 5 ── Beanstalk
    (
        "Beanstalk",
        "Governance improvement proposal votes should not be manipulated. "
        "A transaction that combines a flash loan with a governance vote within "
        "the same execution is a possible indicator of malicious behavior.",
        (
            "voteTX(\n"
            "    is called vote()\n"
            "    is emitted FlashLoan()) occ"
        ),
        BEANSTALK_CONTEXT,
    ),
]


RUN_INDEX = 2  

SLEEP_BETWEEN_CALLS = 3



def run_single(generator, index):
    req_id, requirement, ground_truth, context = TEST_CASES[index]

    print(f"\n{'=' * 70}")
    print(f"[{index}] {req_id}")
    print(f"Requirement: {requirement}")
    print(f"\n GROUND TRUTH:\n{ground_truth}")

    # Mode 1 — prompt only
    result_m1 = generator.generate(requirement)
    print(f"\n MODE 1 (prompt only):\n{result_m1}")

    time.sleep(SLEEP_BETWEEN_CALLS)

    # Mode 2 — prompt + DApp context
    result_m2 = generator.generate(requirement, dapp_context=context)
    print(f"\n MODE 2 (prompt + context):\n{result_m2}")

    print("-" * 70)


def run_evaluation():
    client    = LLMFactory.create(PROVIDER, api_key=API_KEY, model=MODEL)
    generator = RuleGenerator(client)

    print(f"Provider: {client}")
    print(f"Running: {'all cases' if RUN_INDEX is None else f'case {RUN_INDEX} only'}\n")

    if RUN_INDEX is None:
        for i in range(len(TEST_CASES)):
            run_single(generator, i)
            if i < len(TEST_CASES) - 1:
                time.sleep(SLEEP_BETWEEN_CALLS)
    else:
        run_single(generator, RUN_INDEX)


if __name__ == "__main__":
    run_evaluation()