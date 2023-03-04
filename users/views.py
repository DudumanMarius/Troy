from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import RegisterForm


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        message_string = f"Sign Up successfully."
        messages.success(self.request, message_string)
        return super().form_valid(form)
