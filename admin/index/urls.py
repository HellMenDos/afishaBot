from django.conf.urls import url

from index.views import CityList, PostsList, PostsGetOne, PostsGetWithTypes,\
    PostsGetWithHuman, PostsGetWithTitle, PostsGetWithLocation, PostsGetWithBest, \
    PostsListAll, GameAll, GameOne, GameGetHuman, GameGetQuestion, HumanArray, HumanList, \
    TypeOfPostsList, UpdatePaid, PostsCoord, HumanList, PostsGetCount, CityTypeView, SendMap


urlpatterns = [
    url('city/get/?$', CityList.as_view()),
    url('city/type/?$', CityTypeView.as_view()),
    url('types/get/?$', TypeOfPostsList.as_view()),
    url('human/get/?$', HumanList.as_view()),
    url('posts/get/?$', PostsList.as_view()),
    url('posts/all/?$', PostsListAll.as_view()),
    url('post/map/send/(?P<id>[0-9]+)/(?P<chatId>[0-9]+)/?$',
        SendMap.as_view()),
    url('post/coord/(?P<la>[0-9.]+)/(?P<lo>[0-9.]+)/?$',
        PostsCoord.as_view()),
    url('posts/count/(?P<id>[0-9]+)/?$',
        PostsGetCount.as_view()),
    url('post/one/(?P<pk>[0-9]+)/?$', PostsGetOne.as_view()),
    url('post/update/(?P<id>[0-9]+)/(?P<paid>[0-1]+)/?$',
        UpdatePaid.as_view()),
    url('post/types/(?P<day>[0-3]+)/(?P<id>[0-9]+)/?$',
        PostsGetWithTypes.as_view()),
    url('post/human/(?P<id>[0-9]+)/?$', PostsGetWithHuman.as_view()),
    url('post/title/(?P<title>[0-9а-яА-Яa-zA-Z]+)/?$',
        PostsGetWithTitle.as_view()),
    url('post/location/(?P<title>[0-9а-яА-Яa-zA-Z]+)/?$',
        PostsGetWithLocation.as_view()),
    url('post/best/(?P<slug>[0-1]+)/?$',
        PostsGetWithBest.as_view()),
    url('game/all/?$', GameAll.as_view()),
    url('game/one/(?P<pk>[0-9]+)/?$', GameOne.as_view()),
    url('game/human/(?P<id>[0-9]+)/?$', GameGetHuman.as_view()),
    url('game/question/(?P<title>[0-9а-яА-Яa-zA-Z]+)/?$',
        GameGetQuestion.as_view()),

]
