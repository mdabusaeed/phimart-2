from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.utils import email_verification_token
from django.contrib.sites.shortcuts import get_current_site
from users.utils import send_activation_email

User = get_user_model()

# Create your views here.

@api_view(['POST'])
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def resend_activation_email(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        if user.is_active:
            return Response({'message': 'Account is already activated'}, status=status.HTTP_400_BAD_REQUEST)
        
        current_site = get_current_site(request)
        send_activation_email(user, current_site)
        return Response({'message': 'Activation email sent successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
