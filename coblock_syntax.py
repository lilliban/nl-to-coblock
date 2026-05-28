#come convenzione si mette prima la documentazione, poi gli esempi

COBLOCK_DOCS = """
CoBlock is a domain-specific language designed to write compliance and 
security rules for blockchain systems. It is built on two pillars: 
transactions and filters.

TRANSACTIONS (TX)
A transaction represents the execution of a specific operation or function 
within a smart contract. It contains precise data that can be checked, such 
as: who sent the money, which function was triggered, which block it belongs 
to, and how much gas it consumed.

Syntax:
  name(filters) control_flow

FILTERS (FIELD)
Filters are optional criteria you can add when defining a transaction to 
check. If a filter is not included, it means there is no constraint on that 
specific data. Available filters:
  contract  : filter by the smart contract address where the action occurs
  sender    : filter by the address that initiated the transaction
  function  : filter by the name of the executed function
  block     : filter by the blockchain block number
  timestamp : filter by the exact moment (UNIX time) the action occurred
  gas       : filter by gas consumption (e.g. gas > 4000000)

UNARY CONTROL FLOW (one transaction)
The presence or absence of a single transaction is verified using:
  occ  → the transaction MUST be present. 
         If not found, the rule is violated.
  nocc → the transaction must NEVER be present. 
         If found, the rule is violated.

BINARY CONTROL FLOW (two transactions)
Two transactions can be linked using binary constructs, defining time or 
order relations between them. A time interval (TI) is always associated, 
expressed in seconds or number of mined blocks:
  ef  (eventually follows)        : B must happen after A, within the time limit
  df  (directly follows)          : B must happen immediately after A, with no 
                                    other transactions in between
  nef (never eventually follows)  : B must never appear after A
  ndf (never directly follows)    : B must never appear immediately after A

Time interval examples:
  ef < 864000 seconds
  nef > 0 blocks
"""


COBLOCK_EXAMPLES = [
    {
        "nl": "Markets should be resolved with the proper reward. Traders must claim their proceeds in each market",
        "rule": "claimTX(function is ClaimTradingProceeds) nocc"
    },
    {
        "nl": "Avoid excessive fees that could discourage market creation. Maximum 4,000,000 gas units",
        "rule": "createTX(function is CreateMarket gas > 4000000) occ"
    },
    {
        "nl": "All markets should be instantiated by the in-charge smart contract 0x7677 to guarantee correct flow",
        "rule": "createTX(contract is not 0x7677 function is CreateMarket) occ"
    },
    {
        "nl": "Markets should have a reasonable duration. Check for a time frame too close between market creation and finalization — 10 days",
        "rule": "finalizeTX(function is FinalizeMarket)\nef < 864000 seconds\ncreateTX(function is CreateMarket)" 
    }
]


