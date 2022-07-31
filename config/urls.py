"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
#urlpatterns += patterns('', url(r'^silk', include('silk.urls', namespace='silk')))
