from django.contrib import admin
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'sort_order', 'active')


admin.site.register(Question, QuestionAdmin)
