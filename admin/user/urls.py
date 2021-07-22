from django.conf.urls import url

from user.views import UserOne, UserAddPoints, UserList, UserStatTop, UserCheck, UserGetByToken, GameStart, GameGetOne


urlpatterns = [
    url('user/reg/(?P<token>[0-9а-яА-Яa-zA-Z]+)/(?P<city>[0-9а-яА-Яa-zA-Z]+)/?$',
        UserOne.as_view()),
    url('user/get/(?P<token>[0-9а-яА-Яa-zA-Z]+)/?$',
        UserGetByToken.as_view()),
    url('user/check/(?P<token>[0-9а-яА-Яa-zA-Z]+)/?$',
        UserCheck.as_view()),
    url('user/list/',
        UserList.as_view()),
    url('user/add/points/(?P<token>[0-9а-яА-Яa-zA-Z]+)/(?P<points>[0-9]+)/?$',
        UserAddPoints.as_view()),
    url('user/stat/top/(?P<token>[0-9а-яА-Яa-zA-Z]+)/(?P<top>[0-1]+)/(?P<ys>[0-1]+)/(?P<tooday>[0-1]+)/(?P<qest>[0-1]+)/?$',
        UserStatTop.as_view()),
    url('action/create/(?P<token>[0-9а-яА-Яa-zA-Z]+)/(?P<code>[0-1]+)/?$',
        GameStart.as_view()),
    url('action/get/(?P<token>[0-9а-яА-Яa-zA-Z]+)/?$', GameGetOne.as_view()),
]
