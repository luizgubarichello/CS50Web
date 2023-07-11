from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit/<str:entry>", views.edit_page, name="edit_page"),
    path("random_entry", views.random_entry, name="random_entry"),
]
