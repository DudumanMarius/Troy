from django.urls import path
from classes import views

urlpatterns = [
    path("", views.ClassesListView.as_view(), name="list"),
    path("my-classes/", views.MyClassesListView.as_view(), name="my-classes"),
    path("create/", views.CreateClassView.as_view(), name="create"),
    path("view/<int:pk>/", views.ClassView.as_view(), name="view"),
    path("join/<int:pk>/", views.join_class, name="join")
]
