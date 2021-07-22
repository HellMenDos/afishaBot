from rest_framework import serializers
from index.models import City, TypeOfPosts, Human, Posts, Game


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class TypeOfPostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeOfPosts
        fields = '__all__'


class HumanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Human
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = '__all__'
        depth = 1


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'
        depth = 1
