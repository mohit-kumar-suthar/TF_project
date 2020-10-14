from django.core.mail import EmailMessage
from django.template.loader import get_template

def send(msg_type,username,email,token):
    try:
        if msg_type=='register':
            detail="register your account"
            subject="Activation Key"
            page="activate"
        if msg_type=='password':
            detail="reset your password"
            subject="Reset Password"
            page="reset"
        message=get_template('email_templates.html').render({
            'page':page,
            'username':username,
            'token':token,
            'detail':detail,
        })
        msg = EmailMessage(
            subject,
            message,
            'teamfirecode.project@gmail.com',
            [email],
        )
        msg.content_subtype='html'
        msg.send()
    except:
        print('Network Connection error')


