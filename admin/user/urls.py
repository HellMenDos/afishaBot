from django.conf.urls import url

from user.views import UserOne, UserAddPoints, UserList, UserStatTop


urlpatterns = [
    url('user/add/(?P<token>[0-9а-яА-Яa-zA-Z]+)/?$',
        UserOne.as_view()),
    url('user/list/',
        UserList.as_view()),
    url('user/add/points/(?P<token>[0-9а-яА-Яa-zA-Z]+)/(?P<points>[0-9]+)/?$',
        UserAddPoints.as_view()),
    url('user/stat/top/(?P<token>[0-9а-яА-Яa-zA-Z]+)/(?P<top>[0-1]+)/(?P<ys>[0-1]+)/(?P<tooday>[0-1]+)/(?P<qest>[0-1]+)/?$',
        UserStatTop.as_view()),
]
