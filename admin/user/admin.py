from django.contrib import admin
from user.models import User, Actions, Idols, Push, Stat


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'location', 'date')
    list_filter = ('location', 'date')


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'date')
    list_filter = ('user', 'action', 'date')


@admin.register(Actions)
class ActionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question')


@admin.register(Idols)
class IdolsAdmin(admin.ModelAdmin):
    filter_horizontal = ('humans',)


@admin.register(Push)
class PushAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'describe')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = {}
        context.update(extra_context or {})
        context.update(
            {'id': object_id})
        return super().change_view(request, object_id, form_url, context)
