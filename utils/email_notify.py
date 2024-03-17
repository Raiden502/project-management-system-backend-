import requests
from myapp.config import EMAIL_NOTIFY

def notify_mail(endpoint, body):
    try:
        res = requests.post(EMAIL_NOTIFY.API+endpoint,json=body, headers={'Content-Type':'application/json'})
    except Exception as e:
        print("Error in sending mail notification")