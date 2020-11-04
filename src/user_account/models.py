from django.db import models

# Create your models here.

from django.conf import settings
from django.contrib.auth.models import User


class UserAccountProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    image = models.ImageField(default='default.jpg', upload_to='pics')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Profile'
