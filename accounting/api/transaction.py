from ninja import Router
from http import HTTPStatus
from accounting import services
from accounting.exceptions import AtomicAccountTransferException, ZeroAmountError, AccountingEquationError
from accounting.schemas import TransactionIn, TransactionOut, TransactionOutSchema

transaction_router = Router()


# @transaction_router.get('/get-all', response=List[TransactionIn])
# def get_all(request):
#     transactions = Transaction.objects.all()
#
#     return 200, transactions

@transaction_router.post('/add-transaction', response=TransactionOutSchema)
def add_transaction(request, transaction_in: TransactionIn):
    t = services.account_transfer(transaction_in)
    return HTTPStatus.OK, {
        'transaction': t,
        # 'jes': t.journal_entries.all()
    }