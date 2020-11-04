from django.contrib import admin

# Register your models here.
from user_account.models import UserAccountProfile


class UserAccountProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'image')  # , 'user_email')
    list_display = ('user', 'image')  # , 'user_email')

    def user_email(self, instance):
        return instance.user.email


admin.site.register(UserAccountProfile, UserAccountProfileAdmin)
