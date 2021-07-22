from django.shortcuts import render
from rest_framework import generics

from user.models import User, Actions
from user.serilizers import UserSerializer, UserListSerializer, ActionsSerializer, ActionsListSerializer
from rest_framework.response import Response
from index.models import City, Game
from django.db.models import F
import random


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserCheck(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, token):
        data = User.objects.filter(token=token).first()
        if data:
            return Response(data={'have': True})
        else:
            return Response(data={'have': False})


class UserGetByToken(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get(self, request, token):
        data = User.objects.filter(token=token).first()
        serData = UserListSerializer(data).data
        return Response(data=serData)


class UserOne(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, token, city):
        data = User.objects.filter(token=token).first()
        if data:
            print('hello')
            cityId = City.objects.filter(name=city).first().id
            User.objects.filter(token=token).update(location=cityId)
            return Response(data={"status": "success"})
        else:
            cityData, created = City.objects.get_or_create(name=city)
            serializeData = UserSerializer(
                data={"token": token, "location": cityData.id})
            if serializeData.is_valid():
                serializeData.save()
                return Response(data=serializeData.data)
            else:
                return Response(data=serializeData.errors)


class UserAddPoints(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get(self, request, token, points):
        data = User.objects.filter(token=token).update(
            points=F("points") + int(points))
        return Response(data={"token": token, "points": int(points)})


class UserStatTop(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get(self, request, token, top, ys, tooday, qest):
        data = User.objects.filter(token=token).update(
            top=F("top") + int(top), yesterday=F("yesterday") + int(ys), tooday=F("tooday") + int(tooday), questions=F("questions") + int(qest))
        return Response(data={"status": 'success'})


class GameStart(generics.ListAPIView):
    queryset = Actions.objects.all()
    serializer_class = ActionsSerializer

    def get(self, request, token, code):
        userId = User.objects.filter(token=token).first().id
        getGameQuestion = Game.objects.filter(
            photo='') if code else Game.objects.filter(question='')
        randId = random.randint(1, len(getGameQuestion))
        getAction = Actions.objects.filter(user=userId)
        if getAction:
            getAction.update(question=randId)
            serData = ActionsListSerializer(
                Actions.objects.filter(user=userId).first()).data
            return Response(data=serData)
        else:
            saveData = ActionsSerializer({"user": userId, "question": randId})
            if saveData.is_valid():
                saveData.save()
                return Response(data=saveData.data)
            else:
                return Response(data=saveData.errors)


class GameGetOne(generics.ListAPIView):
    queryset = Actions.objects.all()
    serializer_class = ActionsListSerializer

    def get(self, request, token):
        userId = User.objects.filter(token=token).first()
        if userId:
            data = Actions.objects.filter(user=userId.id).first()
            serData = ActionsListSerializer(data).data
            return Response(data=serData)
        else:
            return Response(data={"user": 'fail'})

    def delete(self, request, token):
        userId = User.objects.filter(token=token).first()
        if userId:
            Actions.objects.filter(user=userId.id).delete()
            return Response(data={"status": "success"})
        else:
            return Response(data={"user": 'fail'})
