from django.contrib import messages
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
import json

from django.core.exceptions import ValidationError
from django.forms import URLField
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from tld import get_tld

from surveys.forms import SurveyResponseForm
from surveys.models import SurveyQuestion, Survey, SurveyResponse, SurveyQuestionResponse
from urllib.parse import urlparse

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
        survey = Survey.objects.filter(title="Charity of the Month").first()
        website = request.POST.get("website")

        if website[0:7] != 'http://' and website[0:8] != 'https://':
            website = 'http://' + website
        website = urlparse(website).scheme + '://' + urlparse(website).hostname

        try:
            website = URLField().clean(website)
        except ValidationError:
            messages.error(request, "'" + request.POST.get("website") + "' doesn't appear to be a valid web address. Please check it and try again.")

        if get_tld(website) != 'org':
            messages.error(request, 'Organizations nominated must be non-profit, charitable organzations. If ' + request.POST.get("website") + ' is a charity, please <a href="mailto:info@3cross.coop">get in touch</a> and we will submit your nomination manually.', extra_tags='safe')

        if len(messages.get_messages(request)) == 0:
            sq = SurveyQuestion.objects.filter(short_name=website, survey=survey).first()
            if sq is None:
                try:
                    sq = SurveyQuestion()
                    sq.prompt = BeautifulSoup(requests.get(website).content, features="html.parser").title.string
                    sq.type = SurveyQuestion.YES_NO
                    sq.short_name = website
                    sq.survey = survey
                    sq.save()
                except:
                    messages.error(request, "We are unable to verify the web address you submitted (" + request.POST.get("website") + "). Please check it and try again.")

        if len(messages.get_messages(request)) == 0:
            sqr = survey.get_response_for(request.user).get_question_response_for(sq)
            sqr.answer = "Y"
            sqr.save()

        return redirect('/members/surveys/' + survey.slug + ',' + str(survey.id))

@login_required
def survey_view(request, slug, id, *args, **kwargs):
    survey, survey_url = get_redirected(Survey, {'pk': id}, {'slug': slug})
    if request.method == "GET" and survey_url:
        return redirect(survey_url)

    if request.method == "POST":
        survey_form = SurveyResponseForm(request.POST, survey=survey, user=request.user)
        if survey_form.is_valid():
            survey_form.save()
            messages.success(request, "Your responses have been saved.")
            return redirect(reverse_lazy('profile'))
    else:
        survey_form = SurveyResponseForm(survey=survey, user=request.user)

    template = survey.template if survey.template is not None else "survey.html"

    return render(request, template, {"form": survey_form})
