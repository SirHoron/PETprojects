from django.contrib import admin
from django.urls import path, re_path
from BarCard.views import main, IBA, coctail, contacts, list_coctails

urlpatterns = [
    path("", main),
    path("list/IBA/", IBA),
    path("contacts/", contacts),
    path("list/", list_coctails),
    re_path("list/{20}/", coctail),
]
