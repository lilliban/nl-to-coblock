COBLOCK_DOCS = """
CoBlock: Domain-Specific Language for Compliance Checking on Smart Contract Execution Data

RULE STRUCTURE

RULE ::= TX (control_flow_operator) [TI] TX
       | TX (unary_operator)

A rule consists of one or more transactions (TX) connected by control-flow 
constructs.

TRANSACTION (TX)

TX ::= identifier ( [FIELD] [ATTR]* )

identifier ::= [a-zA-Z][a-zA-Z0-9]*

A transaction represents the execution of a specific operation within a smart 
contract. It can be enriched with filters (FIELD) and attributes (ATTR).

FILTERS (FIELD)

FIELD ::= contract (OP) address
        | sender (OP) address
        | function (OP) function_name
        | block (COMP) value
        | timestamp (COMP) value
        | gas (COMP) value

OP ::= is | is not
COMP ::= = | != | < | <= | > | >=

address       ::= 0x[A-Fa-f0-9]+
function_name ::= [a-zA-Z][a-zA-Z0-9]*
value         ::= number | string | ...

Filters are optional. If omitted, no constraint is applied on that field.

TRANSACTION ATTRIBUTES (ATTR)

ATTR ::= is updated SV (COMP) value      -- state variable check
       | is passed I (COMP) value        -- input parameter check
       | is called CALL                  -- internal call check
       | is emitted E                    -- emitted event check

SV   ::= identifier
I    ::= identifier
CALL ::= call_identifier ( contract (OP) address [is passed I (COMP) value]* )
E    ::= event_name ( [is contained ED (COMP) value]* )
ED   ::= identifier

Multiple ATTR blocks can be chained on the same transaction.
Attributes enable fine-grained checks on transaction internals.

CROSS-TRANSACTION REFERENCES (DOT NOTATION)

DOT_REFERENCE ::= TX_identifier.field

Examples:
  createTX.timestamp        -- timestamp field of createTX
  createTX.sender           -- sender field of createTX
  createTX.BOND             -- custom field BOND of createTX
  createTX.designatedReporter

Dot notation allows referencing data from other transactions within the same rule.
It can be used in FIELD values, ATTR values, and TI expressions.

EXPRESSIONS IN TI

TI_expr ::= value | TX_identifier.field | (TI_expr OP TI_expr)

Examples:
  864000
  (createTX.endTime - createTX.timestamp) + 86400

CONTROL FLOW

UNARY (single transaction):
  occ   -- the transaction MUST be present. If not found, the rule is violated.
  nocc  -- the transaction MUST NEVER be present. If found, the rule is violated.

BINARY (two transactions):
  ef   (eventually follows)       : B must occur after A, within the time limit
  df   (directly follows)         : B must occur immediately after A,
                                    with no other transactions in between
  nef  (never eventually follows) : B must never occur after A
  ndf  (never directly follows)   : B must never occur immediately after A

Transaction Interval (TI) - required for binary constructs:
  < value seconds | blocks   -- within the specified limit
  > value seconds | blocks   -- beyond the specified limit

TI can be specified as:
  - Absolute value:  864000 seconds
  - Absolute value:  10 blocks
  - Expression:      (createTX.endTime - createTX.timestamp) + 86400 seconds
"""

COBLOCK_EXAMPLES = [

    {
        "nl": "Markets should be resolved with the proper reward. Traders must claim their proceeds in each market",
        "rule": "claimTX(function is ClaimTradingProceeds) nocc"
    },

    {
        "nl": "Avoid excessive fees that could discourage market creation. Maximum 4,000,000 gas units",
        "rule": "createTX(function is CreateMarket\n    gas > 4000000) occ"
    },

    {
        "nl": "All markets should be instantiated by the in-charge smart contract 0x7677 to guarantee correct flow",
        "rule": "createTX(contract is not 0x7677\n    function is CreateMarket) occ"
    },

    {
        "nl": "The initial reporter must get properly rewarded",
        "rule": "redeemInitRepTX(function is RedeemAsInitialReporter)\nnef > 0 blocks\nfinalizeTX(function is FinalizeMarket)"
    },

    {
        "nl": "A market must not be created with an end time earlier than the current transaction timestamp. The end time is passed as input parameter.",
        "rule": "createTX(function is CreateMarket\n    is passed endTime (< createTX.timestamp)) nocc"
    },

    {
        "nl": "Markets should have a reasonable duration. Check for a time frame too close between market creation and finalization — 10 days",
        "rule": "finalizeTX(function is FinalizeMarket)\nef < 864000 seconds\ncreateTX(function is CreateMarket)"
    },

    {
        "nl": "The settlement is valid only if the designated reporter submits the report with a Transfer event containing the correct recipient and bond amount, within 24 hours after the market end time",
        "rule": "reportTX(sender is createTX.designatedReporter\n    function is SubmitReport\n    is emitted Transfer(is contained to (= createTX.sender)\n    is contained value (= createTX.BOND)))\nef < (createTX.endTime - createTX.timestamp) + 86400 seconds\ncreateTX(contract is 0x7677 function is CreateMarket)"
    }
]