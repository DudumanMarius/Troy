from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from classes.forms import LessonForm
from classes.models import Lesson, Member


class LessonView(LoginRequiredMixin, DetailView):
    template_name = 'lesson/view.html'
    pk_url_kwarg = 'pk'
    model = Lesson
    login_url = reverse_lazy("users:login")

    def get(self, request, **kwargs):
        try:
            self.object = self.get_object()
            teaching_class = self.object.teaching_class
            if teaching_class.teacher != request.user and not Member.objects. \
                    filter(teaching_class=teaching_class, user=request.user). \
                    exists():
                message_string = f"You are not a member of this class."
                messages.warning(request, message_string)
                return redirect(reverse("dashboard:dashboard"))
        except Http404:
            message_string = f"Lesson does not exist."
            messages.warning(request, message_string)
            return redirect(reverse("dashboard:dashboard"))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class LessonsListView(LoginRequiredMixin, ListView):
    model = Lesson
    paginate_by = 30  # if pagination is desired
    template_name = "lesson/list.html"
    login_url = reverse_lazy("users:login")

    def get_queryset(self):
        classes_pk = list(Member.objects.filter(user=self.request.user).values_list("teaching_class__pk", flat=True))
        filters = [Q(user=self.request.user) | Q(
            teaching_class__pk__in=classes_pk)]
        return Lesson.objects.filter(*filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context


class EditLessonView(LoginRequiredMixin, DetailView):
    template_name = 'lesson/edit.html'
    pk_url_kwarg = 'pk'
    model = Lesson
    login_url = reverse_lazy("users:login")

    def get(self, request, **kwargs):
        try:
            self.object = self.get_object()
            if self.object.user != request.user:
                message_string = f"You are not the creator of this lesson."
                messages.warning(request, message_string)
                return redirect(reverse("dashboard:dashboard"))
        except Http404:
            message_string = f"Lesson does not exist."
            messages.warning(request, message_string)
            return redirect(reverse("dashboard:dashboard"))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CreateLessonView(LoginRequiredMixin, FormView):
    template_name = "lesson/create.html"
    form_class = LessonForm
    login_url = reverse_lazy("users:login")

    def form_valid(self, form):
        request = self.request
        new_lesson = form.save(commit=False)
        new_lesson.user = request.user
        new_lesson.content = f"<h1 style='text-align: center;'>" \
                             f"<strong>{new_lesson.title}</strong></h1>" \
                             f"<h5 style='text-align: right;'>" \
                             f"<strong><em>{new_lesson.user}</em></strong>" \
                             f"</h5><hr>"
        new_lesson.save()
        self.success_url = reverse("lessons:edit", args=[new_lesson.pk])
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateLessonView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


@csrf_exempt
def save_lesson(request, pk):
    if request.method == "POST":
        try:
            lesson = Lesson.objects.get(pk=pk)
            content = request.POST.get("content")
            if content:
                lesson.content = content
                lesson.save(update_fields=["content", "date_edited"])
            return JsonResponse({"info": "Lesson saved."})
        except ObjectDoesNotExist:
            return JsonResponse({"info": "Lesson does not exist."}, status=404)
    else:
        return JsonResponse({"info": "Wrong request."}, status=400)
