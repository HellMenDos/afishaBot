from rest_framework import serializers
from user.models import User, Actions


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        depth = 1


class ActionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actions
        fields = '__all__'


class ActionsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actions
        fields = '__all__'
        depth = 2
