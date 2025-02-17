from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Meep(models.Model):
    summary = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, related_name='meep', on_delete=models.DO_NOTHING)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='meep_like', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user} ({self.created_at:%Y-%m-%d %H:%M}) {self.body}..."


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)
    profile_bio = models.TextField(null=True, blank=True)
    homepage_link = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    pinterest = models.CharField(max_length=200, null=True, blank=True)
    telegram = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username


# create profile when new user signup our web app

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(create_profile, sender=User)
