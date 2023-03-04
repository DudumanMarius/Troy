from django import template

from classes.models import Member, Class

register = template.Library()


@register.simple_tag
def is_member(user_pk, class_pk):
    teaching_class = Class.objects.get(pk=class_pk)
    return Member.objects.filter(
        teaching_class=teaching_class, user__pk=user_pk).exists() or \
        teaching_class.teacher.pk == user_pk
