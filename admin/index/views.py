from django.shortcuts import render
from rest_framework import generics
import requests

from index.models import City, TypeOfPosts, Human, Posts, Game, CityType
from index.serilizers import CitySerializer, TypeOfPostsSerializer, HumanSerializer, PostSerializer, GameSerializer, CityTypeSerializer
from rest_framework.response import Response
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import math
import datetime
from django.db.models import F
import time

nom = Nominatim(user_agent="http")


class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityTypeView(generics.ListCreateAPIView):
    queryset = CityType.objects.all()
    serializer_class = CityTypeSerializer

    def post(self, request):
        get_data = CityType.objects.filter(name=request.data['city'])
        if get_data:
            get_data.update(count=F("count") + 1)
        else:
            CityType.objects.create(name=request.data['city'], count=1)

        return Response(status=201)


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

    def get(self, request, id):
        cityId = requests.get(
            'https://telegramexpert.ru/api/user/get/{0}'.format(id)).json()

        type = TypeOfPosts.objects.all().first().id
        data = Posts.objects.filter(
            typeOfPost=type, city=cityId["location"]["id"], paid=True)

        date = datetime.date.today()

        tooday = len(data.filter(
            timeStart__year=date.year, timeStart__month=date.month, timeStart__day=date.day))
        tomorrow = len(data.filter(timeStart__year=date.year,
                                   timeStart__month=date.month, timeStart__day=date.day + 1))
        weekDate = datetime.date.today() - datetime.timedelta(days=2)
        week = datetime.date.today() + datetime.timedelta(days=6)
        weekCount = len(data.filter(
            timeStart__range=[weekDate.strftime('%Y-%m-%d'), week.strftime('%Y-%m-%d')]))
        best = len(data.filter(theBest=True))
        return Response(data={'tooday': tooday, 'tomorrow': tomorrow, 'week': weekCount, 'best': best})


class PostsGetWithTypes(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, day, id):
        cityId = requests.get(
            'https://telegramexpert.ru/api/user/get/{0}'.format(id)).json()

        type = TypeOfPosts.objects.all().first().id
        data = Posts.objects.filter(
            typeOfPost=type, city=cityId["location"]["id"], paid=True)

        date = datetime.date.today()

        if int(day) == 0:
            dt = data.filter(
                timeStart__year=date.year, timeStart__month=date.month, timeStart__day=date.day)
        elif int(day) == 1:
            dt = data.filter(timeStart__year=date.year,
                             timeStart__month=date.month, timeStart__day=date.day + 1)
        elif int(day) == 2:
            weekDate = datetime.date.today() - datetime.timedelta(days=2)
            week = date + datetime.timedelta(days=6)
            dt = data.filter(
                timeStart__range=[weekDate.strftime('%Y-%m-%d'), week.strftime('%Y-%m-%d')])
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
        data = Posts.objects.filter(id=id).update(paid=paid)
        return Response(data={"status": "ok"})


class PostsGetWithBest(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, slug):
        data = Posts.objects.filter(theBest=slug)
        serializeData = PostSerializer(data, many=True)
        return Response(data=serializeData.data)


class SendMap(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, id, chatId):
        post = Posts.objects.get(pk=id)
        coord = nom.geocode(post.location)
        token = "1882761591:AAHEJh8otU_roGCQ_c0fOKarGFvxl4Wgvoc"
        requests.post(
            f'https://api.telegram.org/bot{token}/sendlocation?chat_id={chatId}&latitude={coord.latitude}&longitude={coord.longitude}')
        return Response(status=201)


class PostsCoord(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, la, lo):
        userData = (la, lo)
        data = Posts.objects.filter(paid=True)
        coordData = []
        finalData = []
        for i in range(0, len(data)):
            coord = nom.geocode(data[i].location)

            if coord:
                coordData.append((math.floor(great_circle(
                    userData, (coord.latitude, coord.longitude)).meters), PostSerializer(data[i]).data))
            else:
                coordData.append((99999999, PostSerializer(data[i]).data))

            coordData.sort(key=lambda data: data[0])
            finalData = coordData[0:3]
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
