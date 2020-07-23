import requests
from django.conf import settings


def slack(message, channel):
    data = {
        'token': 'xoxp-352332787698-352469450885-351644748592-5a20aae6330c35c0c1cd311594cc06d6',
        'channel': 'dev-site' if settings.TARGET_ENV == 'dev' else channel,
        'text': message,
        'username': '3cross.coop',
    }

    requests.post("https://slack.com/api/chat.postMessage", data)


def slack_error(message):
    slack(message, '#website-errors')


def slack_notify(message):
    slack(message, '#staff')
