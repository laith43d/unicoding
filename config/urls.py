from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from accounting.api import account_router, je_router, transaction_router
from restauth.api import auth_router
api = NinjaAPI(
    title='Accounting for All',
    version='0.2',
    description='This is a model preview of a double entry accouting system.',
        csrf=True,
)
api.add_router('account/', account_router)
api.add_router('je/', je_router)
api.add_router('transaction/', transaction_router)
api.add_router('auth/', auth_router)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
    ]