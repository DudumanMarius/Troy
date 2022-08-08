from django.urls import path

from . import views

urlpatterns = [
    path('', views.LessonView.as_view(), name="lesson"),
]