from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=128)
    url = models.CharField(max_length=128)


class Teams(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)


class Channels(models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)


class ChannelLogs(models.Model):
    channel = models.ForeignKey(Channels, on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    message = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()