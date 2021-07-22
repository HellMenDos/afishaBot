from django.contrib import admin
from user.models import User, Actions


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'location', 'top',
                    'tooday', 'yesterday', 'questions')
    list_filter = ('location',)


@admin.register(Actions)
class ActionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question')
