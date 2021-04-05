import requests
from django.conf import settings


def slack(message, channel):
    data = {
        'token': settings.SLACK_TOKEN,
        'channel': 'dev-site' if settings.TARGET_ENV == 'dev' else channel,
        'text': message,
        'username': '3cross.coop',
    }

    requests.post("https://slack.com/api/chat.postMessage", data)


def slack_error(message):
    slack(message, '#website-errors')


def slack_notify(message):
    slack(message, '#staff')
