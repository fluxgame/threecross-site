from django.db import models
from django.urls import reverse

from threecross_site import settings
from autoslug import AutoSlugField


class Survey(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    slug = AutoSlugField(populate_from='title')
    real_time_results = models.BooleanField(blank=False, null=False, default=False)
    max_responses = models.IntegerField(blank=False, null=False, default=0)
    template = models.CharField(max_length=128, blank=True, null=True)
    ajax_template = models.CharField(max_length=128, blank=True, null=True)
    sort_questions = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('survey', kwargs={'slug': self.slug, 'id': self.id})

    @property
    def question_dict(self):
        qd = {}
        for q in self.surveyquestion_set.all():
            qd[q.id] = q
        return qd

    def get_response_for(self, user):
        sr = None
        if user.is_authenticated:
            try:
                sr = SurveyResponse.objects.get(survey=self, user=user)
            except SurveyResponse.DoesNotExist:
                sr = SurveyResponse()
                sr.user = user
                sr.survey = self
                sr.save()

        return sr


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, blank=False, null=False)
    short_name = models.CharField(max_length=256, blank=False, null=False)
    prompt = models.TextField(blank=False, null=False)
    required = models.BooleanField(blank=False, null=False, default=False)
    order = models.IntegerField(blank=False, null=False, default=0)

    YES_NO = "YN"
    FREEFORM = "FF"

    type = models.CharField(
        max_length=3,
        choices=[(YES_NO, 'Yes/No'), (FREEFORM, 'Freeform')],
        default=FREEFORM
    )

    def __str__(self):
        return self.short_name

    @property
    def vote_count(self):
        if self.type == SurveyQuestion.YES_NO:
            return self.surveyquestionresponse_set.filter(answer="Y").count()
        else:
            raise RuntimeError("vote_count called on non-vote question")

    class Meta:
        ordering = ["order"]


class SurveyResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT, blank=False, null=False)

    def get_question_response_for(self, question):
        try:
            sqr = SurveyQuestionResponse.objects.get(survey_response=self, question=question)
        except SurveyQuestionResponse.DoesNotExist:
            sqr = SurveyQuestionResponse()
            sqr.survey_response = self
            sqr.question = question
            sqr.save()

        return sqr

    class Meta:
        unique_together = ('user', 'survey',)


class SurveyQuestionResponse(models.Model):
    survey_response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, blank=False, null=False)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.PROTECT, blank=False, null=False)
    answer = models.TextField()

    class Meta:
        unique_together = ('survey_response', 'question',)
