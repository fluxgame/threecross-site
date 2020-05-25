from django.contrib import admin

# Register your models here.

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'sort_order')


admin.site.register(Question, QuestionAdmin)
