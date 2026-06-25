#vocabolari tecnici DApp

"""
Compact technical context for each supported DApp.
Used in Mode 2 (prompt + context) to give the LLM the vocabulary
it needs to generate precise CoBlock rules without reading full XES logs.
"""

AUGUR_CONTEXT = """
DApp: Augur — decentralized prediction market platform on Ethereum.
Main contract: Universe (address 0x7677)

KNOWN FUNCTION NAMES:
  - CreateMarket     : creates a new betting market
                       inputs: endTime (UNIX timestamp), designatedReporter (address), BOND (REP amount)
  - SubmitInitialReport : sender must be createTX.designatedReporter
                          emits: Transfer(to=createTX.sender, value=createTX.BOND)
  - FinalizeMarket   : closes and finalizes a market outcome
  - RedeemAsInitialReporter : the first reporter redeems their reward
  - ClaimTradingProceeds    : traders claim their share of winnings

LOG STRUCTURE (XES, case-id = market address):
  Fields per event: activity (function name), requester (sender address),
                    timestamp, blockNumber, gas
  One trace = all transactions for one market lifecycle.

EXAMPLE TRACE (market 0xb5f9):
  CreateMarket       | sender=0xc77b | timestamp=1531194451 | gas=6000000
  SubmitInitialReport| sender=0xc77b | timestamp=1531484248 | gas=762725
  FinalizeMarket     | sender=0x0f89 | timestamp=1532563649 | gas=324973
  ClaimTradingProceeds | sender=0xf3ed | timestamp=1532822996 | gas=3000000
"""

PANCAKESWAP_CONTEXT = """
DApp: PancakeSwap — decentralized exchange on BNB Smart Chain.
Main contract: CakeOFT (cross-chain CAKE token bridging)

KNOWN FUNCTION NAMES:
  - transferOwnership : transfers contract ownership to a new address
                        input:  newOwner (address, must not be nil)
                        updates state variable: _owner (must equal newOwner)
                        emits:  OwnershipTransferred(previousOwner, newOwner)
                        NOTE: previousOwner in the event must equal the current sender
  - sendFrom          : sends CAKE tokens from one chain to another
                        must make an internal STATICCALL to LayerZero protocol
                        LayerZero contract address: 0xd675
                        (full address: 00000000000000000000000066a71dcef29a0ffbdbe3c6a460a3b5bc225cd675)

LOG STRUCTURE (XES, case-id = sender address):
  Fields per event: activity, sender, timestamp, blockNumber, gas,
                    inputs (list), storageState (list), events (list), internalTxs (list)
  One trace = all transactions by the same user.

KEY DATA PATTERNS:
  - transOwnTX.sender        → the address invoking transferOwnership
  - transOwnTX.inputs.newOwner → the new owner address passed as input
  - STATICCALL to 0xd675     → required internal call for cross-chain in sendFrom
"""

BEANSTALK_CONTEXT = """
DApp: Beanstalk — decentralized stablecoin protocol with DAO governance on Ethereum.
Governance contract: 0xc1e08

GOVERNANCE MECHANISM:
  - propose          : any BEAN holder submits a BIP (Beanstalk Improvement Proposal)
  - vote             : STALK holders vote on a proposal (weight = token balance)
  - commit           : executes a proposal after standard voting period ends
  - emergencyCommit  : immediately executes a proposal that reaches 2/3 supermajority
  - removeLiquidity  : withdraws staked liquidity after voting

FLASH LOAN CONTEXT:
  - Flash loans from Aave emit a FlashLoan event (from Aave Lending Pool V2: 0x7d276)
  - The governance attack combines: flash loan (→ FlashLoan event) + vote (→ vote() call)
    within a single atomic transaction

KEY ATTACK PATTERN:
  A single transaction that both:
  1. contains an internal call to the vote() function
  2. emits a FlashLoan event
  → indicates possible governance vote manipulation

LOG STRUCTURE (XES, case-id = transaction hash OR sender address):
  Fields per event: functionName, sender, gasUsed, blockNumber, timestamp,
                    internalTxs (list), events (list)

IMPORTANT - occ vs nocc:
  The compliance rule for this scenario uses 'occ' (occurrence), NOT 'nocc'.
  This is because the rule is written to DETECT the attack pattern,
  flagging traces where the manipulation occurred.
  'occ' means: find traces where this transaction IS present (compliant = attack detected).
  'nocc' would mean: flag traces where this transaction appears (non-compliant).
  For attack detection rules, always use 'occ'.                    
"""

DAPP_CONTEXTS = {
    "augur": AUGUR_CONTEXT,
    "pancakeswap": PANCAKESWAP_CONTEXT,
    "beanstalk": BEANSTALK_CONTEXT,
}
