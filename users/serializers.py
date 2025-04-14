from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer, UserSerializer as BaseUserSerializer
from django.contrib.sites.shortcuts import get_current_site
from users.utils import send_activation_email


class UserCreateSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        request = self.context.get('request')
        if request:
            current_site = get_current_site(request)
            send_activation_email(user, current_site)
        return user

class UserSerializer(BaseUserSerializer):
    
    class Meta(BaseUserSerializer.Meta):
        ref_name = "CustomUserSerializer"
        fields = ('id', 'email', 'first_name', 'last_name', 'address', 'phone', 'is_staff')

        read_only_fields = ('is_staff',)    

