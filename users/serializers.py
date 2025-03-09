from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer, UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(BaseUserSerializer):
    
    class Meta(BaseUserSerializer.Meta):
        ref_name = "CustomUserSerializer"
        fields = ('id', 'email', 'first_name', 'last_name', 'address', 'phone')

