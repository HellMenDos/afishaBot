from django.contrib import admin
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'location', 'top',
                    'tooday', 'yesterday', 'questions')
    list_filter = ('location',)
