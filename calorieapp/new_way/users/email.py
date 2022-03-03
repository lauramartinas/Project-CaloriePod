from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template


def email():
    subject = 'Mail subject'
    message = 'Mail body'
    email_from = 'from@calorieapp.com'
    recipient_list = ['martinaslaura123@gmail.com']
    send_mail(subject, message, email_from, recipient_list)


def send_register_mail(user):
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    template = get_template('users/emails/register.html')
    content = template.render(context)

    mail = EmailMultiAlternatives(
        subject='Your account have been registered.',
        body=content,
        to=[user.email],
    )
    mail.content_subtype = 'html'
    mail.send()
