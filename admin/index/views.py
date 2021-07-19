from django.shortcuts import render
from rest_framework import generics

from index.models import City, TypeOfPosts, Human, Posts, Game
from index.serilizers import CitySerializer, TypeOfPostsSerializer, HumanSerializer, PostSerializer, GameSerializer
from rest_framework.response import Response


class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class TypeOfPostsList(generics.ListCreateAPIView):
    queryset = TypeOfPosts.objects.all()
    serializer_class = TypeOfPostsSerializer


class HumanList(generics.ListCreateAPIView):
    queryset = Human.objects.all()
    serializer_class = HumanSerializer


class PostsList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


class PostsGetOne(generics.RetrieveAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


class PostsListAll(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        data = Posts.objects.filter(paid=1)
        serializeData = PostSerializer(data, many=True)
        return Response(data=serializeData.data)


class PostsGetWithTypes(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, id):
        data = Posts.objects.filter(typeOfPost=id)
        serializeData = PostSerializer(data, many=True)
        return Response(data=serializeData.data)


class PostsGetWithHuman(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, id):
        data = Posts.objects.filter(human=id)
        serializeData = PostSerializer(data, many=True)
        return Response(data=serializeData.data)


class PostsGetWithTitle(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, title):
        data = Posts.objects.filter(title__startswith=title)
        serializeData = PostSerializer(data, many=True)
        return Response(data=serializeData.data)


class PostsGetWithLocation(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, slug):
        data = Posts.objects.filter(location__startswith=slug)
        serializeData = PostSerializer(data, many=True)
        return Response(data=serializeData.data)


class PostsGetWithBest(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, slug):
        data = Posts.objects.filter(theBest=slug)
        serializeData = PostSerializer(data, many=True)
        return Response(data=serializeData.data)


class GameAll(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameOne(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameGetHuman(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get(self, request, id):
        data = Posts.objects.filter(human=id)
        serializeData = PostSerializer(data, many=True)
        return Response(data=serializeData.data)


class GameGetQuestion(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get(self, request, slug):
        data = Posts.objects.filter(question__startswith=slug)
        serializeData = PostSerializer(data, many=True)
        return Response(data=serializeData.data)
