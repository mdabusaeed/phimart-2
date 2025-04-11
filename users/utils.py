from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

email_verification_token = EmailVerificationTokenGenerator()

def send_activation_email(user, current_site):
    subject = 'আপনার Phimart অ্যাকাউন্ট অ্যাক্টিভেট করুন'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    
    activation_link = f"{settings.DJOSER['EMAIL_FRONTEND_PROTOCOL']}://{settings.DJOSER['EMAIL_FRONTEND_DOMAIN']}/activate/{uid}/{token}/"
    
    html_message = render_to_string('users/activation_email.html', {
        'user': user,
        'activation_link': activation_link,
        'site_name': settings.DJOSER['EMAIL_FRONTEND_SITE_NAME']
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    ) 