from django.shortcuts import render
from django.views.generic import TemplateView


class LessonView(TemplateView):
    template_name = 'lesson/lesson.html'
