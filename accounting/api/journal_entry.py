from typing import List

from ninja import Router

from accounting.models import JournalEntry
from accounting.schemas import JournalEntryOut

je_router = Router()


@je_router.get('/get-all', response=List[JournalEntryOut])
def get_all(request):
    jes = JournalEntry.objects.all()

    return 200, jes
