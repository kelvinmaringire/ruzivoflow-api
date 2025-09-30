from django.contrib.auth.models import User, Group, Permission

from rest_framework import serializers

from .models import ExtendedUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class ExtendedUserSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = ExtendedUser
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.pic:
            request = self.context.get('request')
            image_url = obj.pic.file.url
            return request.build_absolute_uri(image_url)
        return None

