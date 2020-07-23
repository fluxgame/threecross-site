import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from surveys.forms import SurveyResponseForm
from surveys.models import SurveyQuestion, Survey, SurveyResponse, SurveyQuestionResponse


def get_redirected(queryset_or_class, lookups, validators):
    """
    Calls get_object_or_404 and conditionally builds redirect URL
    """
    obj = get_object_or_404(queryset_or_class, **lookups)
    for key, value in validators.items():
        if value != getattr(obj, key):
            return obj, obj.get_absolute_url()
    return obj, None


@login_required
def ajax_vote_view(request, *args, **kwargs):
    if request.method == 'POST':
        question = SurveyQuestion.objects.get(id=request.POST.get('question_id'))
        vote_status = request.POST.get(SurveyResponseForm.SURVEY_QUESTION_HTML_PREFIX + str(question.id)) == 'on'
        survey = question.survey

        sr = survey.get_response_for(request.user)
        sqr = sr.get_question_response_for(question)
        sqr.answer = "Y" if vote_status else "N"
        sqr.save()

        return HttpResponse(json.dumps({'vote_count': question.vote_count}))
    else:
        return HttpResponse(status=404)


@login_required
def nominate_charity_view(request, *args, **kwargs):
    if request.method == "POST" and request.POST.get("nominate_charity") is not None:
        if survey.title != "Charity of the Month":
            raise RuntimeError("attempt to add charity to non-CoM survey")

        website = request.POST.get("website")

        try:
            sq = SurveyQuestion.objects.get(short_name=website)
        except SurveyQuestion.DoesNotExist:
            sq = SurveyQuestion()
            sq.type = SurveyQuestion.YES_NO
            sq.short_name = website
            try:
                sq.prompt = BeautifulSoup(requests.get(website).content).title.string
                sq.survey = survey
                sq.save()
            except:
                errors.append("Couldn't connect to web address. Please try again.")

        if len(errors) == 0:
            sqr = sr.get_question_response_for(sq)
            sqr.answer = "Y"
            sqr.save()


@login_required
def survey_view(request, slug, id, *args, **kwargs):
    errors = []

    survey, survey_url = get_redirected(Survey, {'pk': id}, {'slug': slug})
    if request.method == "GET" and survey_url:
        return redirect(survey_url)

    sr = survey.get_response_for(request.user)

    if request.method == "POST":
        survey_form = SurveyResponseForm(request.POST, survey=survey, survey_response=sr)
    else:
        survey_form = SurveyResponseForm(survey=survey, survey_response=sr)

    template = survey.template if survey.template is not None else "survey.html"

    return render(request, template, {"form": survey_form, "errors": errors})
