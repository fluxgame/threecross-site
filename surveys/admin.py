from django.contrib import admin

from surveys.models import Survey, SurveyQuestion, SurveyResponse, SurveyQuestionResponse


class SurveyQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('survey_response', 'question')


admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyResponse)
admin.site.register(SurveyQuestionResponse, SurveyQuestionResponseAdmin)

