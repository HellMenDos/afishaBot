from django.shortcuts import render
from rest_framework import generics

from user.models import User, Actions, Idols, Push, Stat
from user.serilizers import UserSerializer, UserListSerializer, ActionsSerializer, ActionsListSerializer, IdolsSerializer, IdolsListSerializer, StatSerializer
from rest_framework.response import Response
from index.models import City, Game, Human, Posts
from index.serilizers import PostSerializer, GameSerializer
from django.db.models import F
import random
import requests
import time
import aiogram.utils.markdown as fmt
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, types
import json


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

    def post(self, request):
        token = request.data['token']
        city = request.data['city']
        data = User.objects.filter(token=token).first()
        if data:

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

        getGameQuestion = Game.objects.filter(question='') if bool(
            int(code)) else Game.objects.filter(photo='')

        randId = getGameQuestion.order_by('?').first()
        getAction = Actions.objects.filter(user=userId)
        if getAction:
            getAction.update(question=randId.id)
            serData = ActionsListSerializer(
                Actions.objects.filter(user=userId).first()).data
            return Response(data=serData)
        else:
            saveData = ActionsSerializer(
                data={"user": userId, "question": randId.id})
            if saveData.is_valid():
                saveData.save()
                return Response(data={"question": GameSerializer(randId).data})
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


class UserSetIdols(generics.ListAPIView):
    queryset = Idols.objects.all()
    serializer_class = IdolsSerializer

    def post(self, request):
        userId = User.objects.filter(token=request.data['token']).first().id
        Idols.objects.filter(user=userId).delete()
        arrayId = []
        for i in range(0, len(request.data['humans'])):
            getHumanId = Human.objects.filter(
                name=request.data['humans'][i]).first().id
            arrayId.append(getHumanId)
        serData = IdolsSerializer(
            data={"user": userId, "humans": arrayId})
        if serData.is_valid():
            serData.save()
        return Response(data=serData.data)


class UserGetIdols(generics.ListAPIView):
    queryset = Idols.objects.all()
    serializer_class = IdolsListSerializer

    def get(self, request, id):
        data = Idols.objects.filter(user=id).first()
        if data:
            serData = IdolsListSerializer(data).data['humans']
            responseData = []
            for i in range(0, len(serData)):
                responseData.append(serData[i]['name'])
            return Response(data=responseData)
        else:
            return Response(data={})


class IdolsGetToken(generics.ListAPIView):
    queryset = Idols.objects.all()
    serializer_class = IdolsListSerializer

    def get(self, request, id):
        data = Idols.objects.filter(humans__in=[id]).first()
        if data:
            return Response(data={"user": data.user.token})
        else:
            return Response(data={})


class Send(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, id):
        getData = Push.objects.get(pk=id)
        getAllUsers = User.objects.filter(location=getData.city)
        datass = []
        for i in range(0, len(getAllUsers)):
            method = "sendMessage"
            token = "1921418522:AAGhuuELsBbOeby0OcjyjlGO5lqAbypl30c"
            url = f"https://api.telegram.org/bot{token}/{method}"
            text = f'<b>{getData.title}</b> \n\n{getData.describe}'

            if getData.photo:
                urlPhoto = 'http://127.0.0.1:8000/media/{0}'.format(
                    getData.photo)
                text += f'{fmt.hide_link(urlPhoto)}'

            data = {"chat_id": getAllUsers[i].token,
                    "text": text,
                    'parse_mode': types.ParseMode.HTML
                    }
            res = requests.post(url, data=data)
            datass.append(res.json())
        return Response(data=datass)


class StatAdd(generics.ListAPIView):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer

    def get(self, request, id, slug):
        getData = User.objects.filter(token=id).first().id
        data = StatSerializer(data={'user': getData, 'action': slug})
        if data.is_valid():
            data.save()
            return Response(data=data.data)
        else:
            return Response(data=data.errors)


class SendIdolsPush(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        instance = Posts.objects.filter(sended=False)
        # .filter(sended=False)
        datass = []
        for j in range(0, len(instance)):
            for i in range(0, len(instance[j].human.all())):
                idolId = instance[j].human.all()[i].id

                userToken = requests.get(
                    f'http://127.0.0.1:8000/api/get/token/idols/{idolId}').json()
                if userToken:
                    method = "sendMessage"
                    token = "1921418522:AAGhuuELsBbOeby0OcjyjlGO5lqAbypl30c"
                    url = f"https://api.telegram.org/bot{token}/{method}"

                    markup = []
                    if instance[j].link:
                        markup.append(
                            [{'text': 'Ссылка на покупку', 'url': instance[j].link}])
                    if instance[j].linkForChat:
                        markup.append(
                            [{'text': 'Ссылка на чат', 'url': instance[j].linkForChat}])
                    if instance[j].linkRegistr:
                        markup.append(
                            [{'text': 'Ссылка на регистрацию', 'url': instance[j].linkRegistr}])

                    photo = ''
                    if instance[j].photo:
                        photo = 'http://127.0.0.1:8000/media/{0}'.format(
                            instance[j].photo)
                    if instance[j].costType == 0:
                        cost = str(instance[j].cost) + \
                            ' р.' if instance[j].cost else 'Бесплатно'
                    elif instance[j].costType == 1:
                        cost = 'Депозит в размере ' + \
                            str(instance[j].cost) + \
                            ' р.' if instance[j].cost else 'Бесплатно'
                    elif instance[j].costType == 2:
                        cost = f"Донат (любая купюра мин: {instance[j].cost} р.)"

                    humans = ''
                    for k in range(0, len(instance[j].human.all())):
                        humans += '{0}'.format(instance[j].human.all()[k].name)
                        if not k == (len(instance[j].human.all()) - 1):
                            humans += ', '

                    data = {"chat_id": userToken['user'],
                            "text": f"<b>{instance[j].title}</b> {fmt.hide_link(photo)}\n\n"
                            f"{instance[j].describe} \n"
                            f"Местоположение: {instance[j].location} \n\n"
                            f"Начало:  <u>{str(instance[j].timeStart).split('+')[0]}</u>\n"
                            f"Вход:  <u>{str(instance[j].timeEnd).split('+')[0]}</u>\n\n"
                            f"Выступает: {humans} \n"
                            f"Цена: {cost} \n",
                            'parse_mode': types.ParseMode.HTML,
                            'reply_markup': json.dumps({'inline_keyboard': markup,
                                                        'resize_keyboard': True,
                                                        'one_time_keyboard': True,
                                                        'selective': True})
                            }
                    res = requests.post(url, data=data)
                    datass.append(res.json())
        instance.update(sended=True)
        return Response(data=datass)
