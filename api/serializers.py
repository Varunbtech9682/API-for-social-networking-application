from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import FriendRequest

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'status')

class FriendRequestActionSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['accept', 'reject'])
