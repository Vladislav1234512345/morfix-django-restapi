from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)

        # Сохраняем изменения профиля
        instance.save()

        return instance