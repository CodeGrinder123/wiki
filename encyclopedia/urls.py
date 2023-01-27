from django.urls import path

from . import views
import entries

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="entry"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/", views.random_page, name="random")
]
