from rest_framework import serializers
from .models import Drink, Post, User


class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = ['id', 'name', 'description']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'userID', 'title', 'body']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID', 'name']
