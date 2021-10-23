import smtplib
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer

from seafarer import settings


def send_email(subject,recipient_email,message):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('seafarer.intl@gmail.com', 'seafarer.intl.2021')
    sender = 'Seafarer International <seafarer.intl@gmail.com>'
    msg = MIMEText(message,'html')

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient_email

    server.sendmail(sender, [recipient_email], msg.as_string())
    server.quit()

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt=settings.SECURITY_PASSWORD_SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=settings.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email



