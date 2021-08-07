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
    list_display = ('id', 'title', 'describe',
                    'typeOfPost', 'timeStart', 'paid', 'theBest', 'location', 'costType')
    list_filter = ('human', 'typeOfPost', 'paid', 'location',
                   'sended', 'theBest', 'timeStart', 'costType')
    change_links = ('human', 'typeOfPost')
    readonly_fields = ('paid',)
    filter_horizontal = ('human',)

    def add_view(self, request, form_url='', extra_context=None):
        context = {}
        context.update({"create": False})
        return super().add_view(request, form_url, context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = {}
        context.update(extra_context or {})
        getPaid = Posts.objects.filter(id=object_id).first().paid
        context.update(
            {'id': object_id, "create": True, 'status': request.user.is_superuser, "paid": getPaid, "send": 1 if request.user.is_superuser else 0})
        print(request)
        return super().change_view(request, object_id, form_url, context)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'human', 'question', 'photo', 'points')
    list_filter = ('human', 'question', 'points')
    change_links = ('human', )
