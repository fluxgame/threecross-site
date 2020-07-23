import csv
import dateparser
import pytz
from datetime import datetime
from surveys.models import SurveyQuestion, SurveyResponse, Survey, SurveyQuestionResponse
from users.models import User, Group
from members.models import Member
from addresses.models import Address
from transactions.models import Transaction
from items.models import Item


def save_question_response(survey_response, question, response):
    sqr = SurveyQuestionResponse()
    sqr.answer = response
    sqr.question = question
    sqr.survey_response = survey_response
    sqr.save()


common_item = Item.objects.filter(name=Member.COMMON).first()
preferred_item = Item.objects.filter(name=Member.PREFERRED).first()

t_and_c_question = SurveyQuestion.objects.filter(short_name='t_and_c').first()
bene_question = SurveyQuestion.objects.filter(short_name='bene').first()
referral_question = SurveyQuestion.objects.filter(short_name='referral').first()
improve_question = SurveyQuestion.objects.filter(short_name='improvements').first()
when_question = SurveyQuestion.objects.filter(short_name='when').first()
why_question = SurveyQuestion.objects.filter(short_name='why').first()
skills_question = SurveyQuestion.objects.filter(short_name='skills').first()
est = pytz.timezone('US/Eastern')
application_survey = Survey.objects.get(title='Membership Application Questions')

members_group = Group.objects.get(name='Consumer-Members')
workers_group = Group.objects.get(name='Worker-Members')
pending_group = Group.objects.get(name='Pending Applications')

with open('/Users/flux/Desktop/members.csv') as csvfile:
    member_csv = csv.reader(csvfile)
    for row in member_csv:
        if row[5] == "dave@3cross.coop":
            user = User.objects.get(email='dave@3cross.coop')
        else:
            user = User()
            user.email = row[5]
            user.save()

        address = Address()
        address.user = user
        address.street = row[8]
        address.unit = row[9]
        address.city = row[10]
        address.state = row[11]
        address.postal_code = row[12]
        address.phone_number = row[13]
        address.save()

        member = Member()
        member.user = user
        member.first_name = row[6]
        member.last_name = row[7]
        if len(row[0]) > 0:
            member.number = int(row[0])
        member.save()

        sr = SurveyResponse()
        sr.user = user
        sr.survey = application_survey
        sr.save()

        for line in row[17].splitlines():
            refer_prefix = "Referred By: "
            why_prefix = "Why: "
            when_prefix = "How Long: "
            improve_prefix = "Improvements: "
            skills_prefix = "Skills: "

            if line.startswith(refer_prefix):
                save_question_response(sr, referral_question, line.replace(refer_prefix, ''))
            elif line.startswith(why_prefix):
                save_question_response(sr, why_question, line.replace(why_prefix, ''))
            elif line.startswith(when_prefix):
                save_question_response(sr, when_question, line.replace(when_prefix, ''))
            elif line.startswith(improve_prefix):
                save_question_response(sr, improve_question, line.replace(improve_prefix, ''))
            elif line.startswith(skills_prefix):
                save_question_response(sr, skills_question, line.replace(skills_prefix, ''))

        save_question_response(sr, t_and_c_question, 'Y')
        save_question_response(sr, bene_question, 'Y')

        if len(row[1]) > 0:
            t = Transaction()
            t.user = user
            t.date = est.localize(dateparser.parse(row[1]))
            t.item = common_item
            t.qty = 1
            t.amount = 150
            t.save()
            members_group.user_set.add(user)
        else:
            pending_group.user_set.add(user)

        preferred_shares = 0
        if len(row[21]) > 0:
            preferred_shares = int(row[21])

        if preferred_shares > 0:
            t = Transaction()
            t.user = user
            t.date = est.localize(datetime.today())
            t.item = preferred_item
            t.qty = preferred_shares
            t.amount = preferred_shares * 100
            t.save()

        print(user.full_name)

members_group.save()
pending_group.save()
