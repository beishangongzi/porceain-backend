from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


def avatar_directory(instance, filename):
    return f"avatar/{instance.username}/avatar.png"


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, null=True, unique=True)
    phone = models.CharField(max_length=11, null=False, unique=True)
    password = models.CharField(max_length=200, null=True)
    avatar = models.ImageField(upload_to="user_directory")
    is_vip = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    vip_expire = models.DateTimeField(null=True)

    USERNAME_FIELD = "username"

    def get_username(self):
        username = super(User, self).get_username()
        if username is None:
            username = self.phone
        return username



