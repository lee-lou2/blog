from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=100, verbose_name="제목")
    body = models.TextField(verbose_name="내용")
    sub_title = models.CharField(
        max_length=255, verbose_name="부제목", blank=True, default=""
    )
    image_url = models.URLField(verbose_name="이미지 URL", blank=True, default="")

    class Meta:
        db_table = "content"
        verbose_name = "콘텐츠"
