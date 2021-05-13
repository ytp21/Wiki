from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryname>", views.page, name="entrypage"),
    path("search_result", views.search, name="search"),
    path("new_page", views.newPage, name="newpage"),
    path("edit_page", views.editPage, name="editpage"),
    path("random_page", views.randomPage, name="randompage")
]

