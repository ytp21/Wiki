from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryname>", views.page, name="entrypage"),
    path("search_result", views.search, name="search")
]

