from django.contrib import admin

from classes.models import Class, Member, Lesson


class ClassAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "teacher", "started_on")
    search_fields = ("id", "teacher", "name")


class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "teaching_class")
    search_fields = ("id", )


class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "teaching_class",
                    "date_edited", "date_created")
    list_filter = ("teaching_class", )
    search_fields = ("id", "title")


admin.site.register(Class, ClassAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Lesson, LessonAdmin)
