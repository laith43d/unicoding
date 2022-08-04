from typing import List

from ninja import Router

import accounting.models
from accounting.schemas import JournalEntryOut

je_router = Router()


@je_router.get('/get-all', response=List[JournalEntryOut])
def get_all(request):
    jes = accounting.models.JournalEntry.objects.all()

    return 200, jes
