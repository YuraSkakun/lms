from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from user_account.models import UserAccountProfile


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs# noqa):
#     if created:
#         UserAccountProfile.objects.create(user=instance)
#         print('created')
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if instance.profile:
#         instance.profile.save()

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    # print('This is signal')
    if created:
        UserAccountProfile.objects.create(user=instance)
    else:
        instance.profile.save()
