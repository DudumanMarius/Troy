from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, DetailView

from classes.forms import ClassForm
from classes.models import Class, Lesson, Member


class ClassesListView(LoginRequiredMixin, ListView):
    model = Class
    paginate_by = 30  # if pagination is desired
    template_name = "classes/list.html"
    login_url = reverse_lazy("users:login")

    def get_queryset(self):
        return Class.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context


class MyClassesListView(LoginRequiredMixin, ListView):
    model = Class
    paginate_by = 30  # if pagination is desired
    template_name = "classes/list.html"
    login_url = reverse_lazy("users:login")

    def get_queryset(self):
        classes_pk = list(Member.objects.filter(
            user=self.request.user).values_list(
            "teaching_class__pk", flat=True))
        filters = [Q(teacher=self.request.user) | Q(pk__in=classes_pk)]
        return Class.objects.filter(*filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context


class CreateClassView(LoginRequiredMixin, FormView):
    template_name = "classes/create.html"
    form_class = ClassForm
    success_url = reverse_lazy("classes:my-classes")
    login_url = reverse_lazy("users:login")

    def form_valid(self, form):
        request = self.request
        new_class = form.save(commit=False)
        new_class.teacher = request.user
        new_class.save()
        message_string = f"Class {new_class.name} created successfully."
        messages.success(request, message_string)
        return super().form_valid(form)


class ClassView(LoginRequiredMixin, DetailView):
    template_name = "classes/view.html"
    pk_url_kwarg = 'pk'
    model = Class
    login_url = reverse_lazy("users:login")

    def get(self, request, **kwargs):
        try:
            self.object = self.get_object()
            if self.object.teacher != request.user and not Member.objects. \
                    filter(teaching_class=self.object, user=request.user). \
                    exists():
                message_string = f"You are not a member of this class."
                messages.warning(request, message_string)
                return redirect(reverse("dashboard:dashboard"))
        except Http404:
            message_string = f"Class does not exist."
            messages.warning(request, message_string)
            return redirect(reverse("dashboard:dashboard"))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lessons"] = Lesson.objects.filter(teaching_class=self.object).order_by("-pk")
        return context


@login_required
def join_class(request, pk):
    try:
        teaching_class = Class.objects.get(pk=pk)
        Member.objects.create(teaching_class=teaching_class, user=request.user)
        return redirect(reverse("classes:view", args=[teaching_class.pk]))
    except ObjectDoesNotExist:
        return redirect(reverse("classes:list"))
