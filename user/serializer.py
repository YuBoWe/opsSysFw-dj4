from rest_framework.serializers import ModelSerializer
from .models import UserProfile
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Permission, ContentType, Group


class ContentTypeSerializers(ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class PermSerializers(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

    content_type = ContentTypeSerializers(read_only=True)


class UserSerializers(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'is_superuser', 'email', 'is_active', 'phone', 'password']
        extra_kwargs = {
            'username':  {'max_length': 9, "min_length": 3},
            'password': {"write_only": True},
            'is_superuser': {"default": False},
            'is_active': {"default": False}
        }

    def validate_password(self, value):
        if 6 <= len(value) <= 15:
            return make_password(value)
        raise ValidationError('密码有误')
