from django.shortcuts import render
from rest_framework import generics

from user.models import User
from user.serilizers import UserSerializer, UserListSerializer
from rest_framework.response import Response
from index.models import City
from django.db.models import F


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserOne(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, token):
        data = User.objects.filter(token=token).first()
        if data:
            serializeData = UserSerializer(data)
            return Response(data=serializeData.data)
        else:
            serializeData = UserSerializer(
                data={"token": token, "location": City.objects.all().first().id})
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
