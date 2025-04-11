from django.urls import path
from users.views import activate_user, resend_activation_email

urlpatterns = [
    path('activate/<str:uidb64>/<str:token>/', activate_user, name='activate_user'),
    path('resend-activation/', resend_activation_email, name='resend_activation_email'),
] 