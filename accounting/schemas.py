from decimal import Decimal
from typing import List

from ninja import Schema


class FourOFourOut(Schema):
    detail: str


class AccountOut(Schema):
    id: int
    parent: 'AccountOut' = None
    name: str
    type: str
    code: str
    full_code: str


AccountOut.update_forward_refs()

class TransactionOut(Schema):
    type: str
    description: str

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
    account: str
    balance: List[CurrencyBalance]
    jes: List[JournalEntryOut]
