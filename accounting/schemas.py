from decimal import Decimal
from typing import List, Optional

from ninja import Schema


class FourOFourOut(Schema):
    detail: str


class AccountOut(Schema):
    id: int
    parent: 'AccountOut' = None
    name: str
    type: str
    code: str = None
    full_code: str = None


AccountOut.update_forward_refs()


class StandAloneJournalEntry(Schema):
    id: int
    amount: Decimal
    currency: str


class TransactionOut(Schema):
    type: str
    description: str


class TransactionOutSchema(Schema):
    transaction: TransactionOut
    # jes: List[StandAloneJournalEntry]


class JournalEntry(Schema):
    account: AccountOut
    transaction: TransactionOut
    amount: Decimal
    currency: str


class JournalEntryOut(JournalEntry):
    id: int


class JournalEntryIn(JournalEntry):
    pass


class JournalEntryInTransaction(Schema):
    credit_account: int
    debit_account: int
    amount: Decimal
    currency: str


class TransactionIn(Schema):
    type: str
    description: str
    je: JournalEntryInTransaction


class CurrencyBalance(Schema):
    currency: str
    sum: str


class GeneralLedgerOut(Schema):
    id :int
    parent_id : Optional[int]
    account: str
    balance: List[CurrencyBalance]
    #children : List['GeneralLedgerOut'] =None
    # jes: List[JournalEntryOut]
