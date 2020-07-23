from django.contrib import admin

from surveys.models import Survey, SurveyQuestion, SurveyResponse, SurveyQuestionResponse

admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyResponse)
admin.site.register(SurveyQuestionResponse)

