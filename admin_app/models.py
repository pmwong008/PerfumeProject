from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="user_avatar", null=True, blank=True,default="user_avatar/default_avatar.png")

    def delete(self, *args, **kwargs):
        if self.avatar and self.avatar.name != "user_avatar/default_avatar.png":
            self.avatar.delete(save=False)
        super().delete(*args, **kwargs)

