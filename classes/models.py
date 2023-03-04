from django.db import models

from users.models import User


class Class(models.Model):
    name = models.CharField(verbose_name="Name", max_length=256)
    description = models.TextField(verbose_name="Description")
    teacher = models.ForeignKey(
        User, verbose_name="Teacher", on_delete=models.CASCADE)
    started_on = models.DateField(verbose_name="Started On", auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.teacher}"

    @property
    def get_short_name(self):
        return "".join(
            [x[0] if x[0].isupper() else "" for x in self.name.split(" ")])

    @property
    def number_of_members(self):
        return Member.objects.filter(teaching_class=self).count()


class Member(models.Model):
    user = models.ForeignKey(
        User, verbose_name="User", on_delete=models.CASCADE)
    teaching_class = models.ForeignKey(
        Class, verbose_name="Class", on_delete=models.CASCADE)
    date_joined = models.DateField(
        verbose_name="Date Joined", auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.teaching_class.name}"


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    user = models.ForeignKey(
        User, verbose_name="User", on_delete=models.CASCADE)
    teaching_class = models.ForeignKey(
        Class, verbose_name="Class", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Content", blank=True, null=True)
    date_created = models.DateField(
        verbose_name="Date Joined", auto_now_add=True)
    date_edited = models.DateField(verbose_name="Date Joined", auto_now=True)

    def __str__(self):
        return self.title

    @property
    def get_short_title(self):
        return "".join(
            [x[0] if x[0].isupper() else "" for x in self.title.split(" ")])
