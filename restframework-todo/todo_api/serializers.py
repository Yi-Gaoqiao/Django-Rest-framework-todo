from rest_framework import serializers

from todo_api import models


class UserSerializer(serializers.ModelSerializer):
    """Serialize a user object"""
    class Meta():
        model = models.User
        fields = (
            'id', 'email', 'display_name',
            'password', 'about', 'avatar_url'
        )
        extra_kwargs = {
            'email': {
                'write_only': True,
            },
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'about': {
                'allow_blank': True,
            },
            'avatar_url': {
                'allow_blank': True,
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.User.objects.create_user(
            email=validated_data['email'],
            display_name=validated_data['display_name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class TodoItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    # Get foreign key reference as an object, not a key value
    user = UserSerializer(read_only=True)

    class Meta():
        model = models.TodoItem
        fields = (
            'id', 'user', 'created_at',
            'title', 'content', 'is_finished'
        )
        extra_kwargs = {'user': {'read_only': True}}
