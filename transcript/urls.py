from django.urls import path

from transcript import views

urlpatterns = [
    path("", views.LessonsListView.as_view(), name="list"),
    path('<int:pk>/', views.LessonView.as_view(), name="view"),
    path('create/', views.CreateLessonView.as_view(), name="create"),
    path('edit/<int:pk>/', views.EditLessonView.as_view(), name="edit"),
    path('save/<int:pk>/', views.save_lesson, name="save")
]
