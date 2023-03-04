from django.forms import ModelForm

from classes.models import Class, Lesson


class ClassForm(ModelForm):

    class Meta:
        model = Class
        fields = ("name", "description")


class LessonForm(ModelForm):

    class Meta:
        model = Lesson
        fields = ("title", "teaching_class")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields["teaching_class"].queryset = \
            Class.objects.filter(teacher=self.request.user)
