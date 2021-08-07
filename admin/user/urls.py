from django.conf.urls import url

from user.views import UserOne, UserAddPoints, UserList, UserStatTop, UserCheck, UserGetByToken, GameStart, GameGetOne, UserSetIdols, UserGetIdols, Send, StatAdd, SendIdolsPush, IdolsGetToken


urlpatterns = [
    url('user/reg/?$',
        UserOne.as_view()),
    url('user/get/(?P<token>[0-9а-яА-Яa-zA-Z]+)/?$',
        UserGetByToken.as_view()),
    url('user/idols/get/(?P<id>[0-9]+)/?$',
        UserGetIdols.as_view()),
    url('user/check/(?P<token>[0-9а-яА-Яa-zA-Z]+)/?$',
        UserCheck.as_view()),
    url('user/list/',
        UserList.as_view()),
    url('user/stat/top/(?P<token>[0-9а-яА-Яa-zA-Z]+)/(?P<top>[0-1]+)/(?P<ys>[0-1]+)/(?P<tooday>[0-1]+)/(?P<qest>[0-1]+)/?$',
        UserStatTop.as_view()),
    url('action/create/(?P<token>[0-9а-яА-Яa-zA-Z]+)/(?P<code>[0-1]+)/?$',
        GameStart.as_view()),
    url('action/get/(?P<token>[0-9а-яА-Яa-zA-Z]+)/?$', GameGetOne.as_view()),
    url('user/idols/?$', UserSetIdols.as_view()),
    url('push/send/(?P<id>[0-9]+)/?$', Send.as_view()),
    url('stat/add/(?P<id>[0-9]+)/(?P<slug>[0-9а-яА-Яa-zA-Z]+)/?$',
        StatAdd.as_view()),
    url('send/idols/?$',
        SendIdolsPush.as_view()),
    url('get/token/idols/(?P<id>[0-9]+)/?$',
        IdolsGetToken.as_view()),
]
