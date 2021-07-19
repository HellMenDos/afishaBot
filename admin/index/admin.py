from django.contrib import admin
from index.models import City, TypeOfPosts, Human, Posts, Game

admin.site.site_header = 'Админка бота'


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'describe')


@admin.register(TypeOfPosts)
class TypeOfPostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'describe')


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'describe')


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('title__startswith',)
    list_display = ('id', 'title', 'describe', 'typeOfPost',
                    'human', 'timeStart', 'paid')
    list_filter = ('human', 'typeOfPost', 'paid', 'location')
    change_links = ('human', 'typeOfPost')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'human', 'question', 'points')
    list_filter = ('human', 'question', 'points')
    change_links = ('human', )
