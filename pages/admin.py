from django.contrib import admin
from .models import Question, Announcement


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'sort_order', 'active')


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'text')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
