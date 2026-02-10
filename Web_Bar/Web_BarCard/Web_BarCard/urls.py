from django.contrib import admin
from django.urls import path, re_path
from BarCard.views import main, IBA, coctail, contacts, list_coctails, admin, error_page

urlpatterns = [
    path("", main),
    re_path(r"^IBA/$", IBA),
    re_path(r"^contacts/$", contacts),
    re_path(r"^list/page-\d+/$", list_coctails),
    re_path(r"^list/coctail/\D+/$", coctail),
    path("admin/", admin),
    re_path(r"^\D+/", error_page),
]
