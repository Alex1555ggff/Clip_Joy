import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

def generate_unique_name():
    #Генератор уникального названия канала
    return f'user_{uuid.uuid4().hex}'

class User(AbstractUser):
    name = models.CharField(max_length=150, unique=True, default=generate_unique_name)
    logo = models.ImageField(upload_to='channel_images/', default='channel_images/AnonymUser.png')
    description = models.TextField(blank=True, null=True, max_length=1024,)
    subscribers = models.ManyToManyField("User", related_name='subscribed_users')

    class Meta:
        ordering = ['-username']

    def is_subscribed(self, other_user):
        return self.subscribers.filter(id=other_user.id).exists()

    def __str__(self):
        return self.name

 
class Video(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    video = models.FileField(
        upload_to='videos/videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],)
    
    photo = models.ImageField(upload_to='videos/images/')
    views = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_users')
    disliked_by = models.ManyToManyField(User, related_name='disliked_users')
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    pub_date = models.DateTimeField(auto_now_add=True)

    def reaction_checks(self, user):
        if self.liked_by.filter(pk = user.pk).exists():
            return "like"
        elif self.disliked_by.filter(pk = user.pk).exists():
            return "dislike"
        else:
            return False

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(max_length=512)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)



