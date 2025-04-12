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

@api_view(['GET'])
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response(
            {'message': 'Invalid activation link or user not found'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    if user.is_active:
        return Response(
            {'message': 'Account is already activated'}, 
            status=status.HTTP_200_OK
        )

    if email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response(
            {'message': 'Account activated successfully'}, 
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'message': 'Invalid or expired activation link'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def resend_activation_email(request):
    email = request.data.get('email')
    if not email:
        return Response(
            {'message': 'Email is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)
        if user.is_active:
            return Response(
                {'message': 'Account is already activated'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        current_site = get_current_site(request)
        send_activation_email(user, current_site)
        return Response(
            {'message': 'Activation email sent successfully'}, 
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(
            {'message': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )