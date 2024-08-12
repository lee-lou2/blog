from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=50)
    image_url = models.URLField()

    class Meta:
        db_table = "user_profile"
        verbose_name = "유저 프로필"
        verbose_name_plural = "유저 프로필"
