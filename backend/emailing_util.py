from flask_mail import Message
from .mail import mail


def send_email(receivers, message, title):
    msg = Message(title, sender='eltranscriber.email@gmail.com', recipients=receivers)
    msg.body = message
    mail.send(msg)
    return "success"
