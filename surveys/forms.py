from django import forms
from django.utils.safestring import mark_safe

from surveys.models import SurveyQuestion
from django.conf import settings


class SurveyFieldMixin:
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        self.response = kwargs.pop('response')
        kwargs['label'] = mark_safe(self.question.prompt)
        kwargs["required"] = self.question.required
        super(SurveyFieldMixin, self).__init__(*args, **kwargs)


class YesNoField(SurveyFieldMixin, forms.Field):
    widget = forms.CheckboxInput

    def __init__(self, *args, **kwargs):
        super(YesNoField, self).__init__(*args, **kwargs)
        if self.response is not None:
            self.initial = self.response.answer == "Y"
        elif self.question.required and settings.TARGET_ENV == "dev":
            self.initial = True

    def to_python(self, value):
        if isinstance(value, str) and value.lower() in ('false', '0'):
            value = "N"
        else:
            value = "Y" if bool(value) else "N"
        return super().to_python(value)


class FreeFormField(SurveyFieldMixin, forms.CharField):
    def __init__(self, *args, **kwargs):
        super(FreeFormField, self).__init__(*args, **kwargs)
        self.widget = forms.Textarea(attrs={'rows': 1})
        if self.response is not None:
            self.initial = self.response.answer
        elif self.question.required and settings.TARGET_ENV == "dev":
            self.initial = 'a'


class SurveyResponseForm(forms.BaseForm):
    SURVEY_QUESTION_HTML_PREFIX = 'sq-'

    def __init__(self, *args, survey, survey_response, **kwargs):
        self.survey = survey
        self.instance = survey_response
        self.base_fields = {}
        for survey_question in survey.surveyquestion_set.all():
            sqr = None if survey_response is None else survey_response.get_question_response_for(survey_question)
            if survey_question.type == SurveyQuestion.YES_NO:
                field = YesNoField(question=survey_question, response=sqr)
            elif survey_question.type == SurveyQuestion.FREEFORM:
                field = FreeFormField(question=survey_question, response=sqr)
            else:
                raise RuntimeError("survey question type '" + survey_question.type + "' not implemented.")

            self.base_fields[SurveyResponseForm.SURVEY_QUESTION_HTML_PREFIX + str(survey_question.pk)] = field

        super(SurveyResponseForm, self).__init__(*args, **kwargs)

        if self.is_valid():
            qd = survey.question_dict
            for name, datum in self.cleaned_data.items():
                q_id = int(name.replace(SurveyResponseForm.SURVEY_QUESTION_HTML_PREFIX, ''))
                sqr = self.instance.get_question_response_for(qd[q_id])
                sqr.answer = datum
                print(sqr.answer)
                sqr.save()

    # def save(self):
    #     self.instance.save()
    #     for sqr in self.instance.surveyquestionresponse_set.all():
    #         print(sqr.answer)
    #         sqr.save()
