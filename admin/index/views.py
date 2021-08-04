from django.shortcuts import render
from rest_framework import generics

from index.models import City, TypeOfPosts, Human, Posts, Game
from index.serilizers import CitySerializer, TypeOfPostsSerializer, HumanSerializer, PostSerializer, GameSerializer
from rest_framework.response import Response
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import math
import datetime
import time
nom = Nominatim(user_agent="http")


class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class TypeOfPostsList(generics.ListCreateAPIView):
    queryset = TypeOfPosts.objects.all()
    serializer_class = TypeOfPostsSerializer


class HumanList(generics.ListCreateAPIView):
    queryset = Human.objects.all()
    serializer_class = HumanSerializer


class HumanArray(generics.ListAPIView):
    queryset = Human.objects.all()
    serializer_class = HumanSerializer

    def get(self, request):
        data = Human.objects.all()
        arrayOfHumans = []
        for i in range(0, len(data)):
            arrayOfHumans.append(data[i].name)
        return Response(data={"data": arrayOfHumans})


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


class PostsGetCount(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        type = TypeOfPosts.objects.all().first().id
        data = Posts.objects.filter(typeOfPost=type)

        date = datetime.date.today()

        tooday = len(data.filter(
            timeStart__year=date.year, timeStart__month=date.month, timeStart__day=date.day))
        tomorrow = len(data.filter(timeStart__year=date.year,
                                   timeStart__month=date.month, timeStart__day=date.day + 1))
        weekDate = datetime.date.today() + datetime.timedelta(days=1)
        week = date + datetime.timedelta(days=7)
        weekCount = len(data.filter(
            timeStart__range=[week.strftime('%Y-%m-%d'), weekDate.strftime('%Y-%m-%d')]))
        best = len(data.filter(theBest=True))
        return Response(data={'tooday': tooday, 'tomorrow': tomorrow, 'week': weekCount, 'best': best})


class PostsGetWithTypes(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, day):
        type = TypeOfPosts.objects.all().first().id
        data = Posts.objects.filter(typeOfPost=type)

        date = datetime.date.today()

        if int(day) == 0:
            dt = data.filter(
                timeStart__year=date.year, timeStart__month=date.month, timeStart__day=date.day)
        elif int(day) == 1:
            dt = data.filter(timeStart__year=date.year,
                             timeStart__month=date.month, timeStart__day=date.day + 1)
        elif int(day) == 2:
            weekDate = datetime.date.today() + datetime.timedelta(days=1)
            week = date + datetime.timedelta(days=7)
            dt = data.filter(
                timeStart__range=[week.strftime('%Y-%m-%d'), weekDate.strftime('%Y-%m-%d')])
        else:
            dt = data.filter(theBest=True)

        serializeData = PostSerializer(dt, many=True)
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


class UpdatePaid(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, id, paid):
        if paid:
            data = Posts.objects.filter(id=id).update(paid=True)
            return Response(data={"status": "ok"})
        else:
            return Response(data={"status": "false"})


class PostsGetWithBest(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, slug):
        data = Posts.objects.filter(theBest=slug)
        serializeData = PostSerializer(data, many=True)
        return Response(data=serializeData.data)


class PostsCoord(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, la, lo):
        userData = (la, lo)
        data = Posts.objects.all()
        coordData = []
        finalData = []
        for i in range(0, len(data)):
            coord = nom.geocode(data[i].location)

            if coord:
                coordData.append((math.floor(great_circle(
                    userData, (coord.latitude, coord.longitude)).meters), PostSerializer(data[i]).data))
            else:
                coordData.append((99999999, PostSerializer(data[i]).data))

            coordData.sort()
            finalData = coordData[0:4]
        return Response(data=finalData)


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
