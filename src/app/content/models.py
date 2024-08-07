from django.contrib.auth.models import User
from django.db import models


class Content(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="contents",
        verbose_name="작성자 ID",
    )
    title = models.CharField(max_length=100, verbose_name="제목")
    body = models.TextField(verbose_name="내용")
    sub_title = models.CharField(
        max_length=255, verbose_name="부제목", blank=True, default=""
    )
    image_url = models.URLField(verbose_name="이미지 URL", blank=True, default="")

    class Meta:
        db_table = "content"
        verbose_name = "콘텐츠"


class ContentComment(models.Model):
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name="content_comments",
        verbose_name="콘텐츠",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="reply_comments",
        verbose_name="부모 댓글",
        null=True,
        blank=True,
    )
    body = models.CharField(max_length=255, verbose_name="내용")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="content_comments",
        verbose_name="��용자",
    )
    created_at = models.DateTimeField(verbose_name="생성일시", auto_now_add=True)

    class Meta:
        db_table = "content_comment"
        verbose_name = "콘텐츠 댓글"
        verbose_name_plural = verbose_name


class ContentTag(models.Model):
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name="content_tags",
        verbose_name="콘텐츠",
    )
    tag = models.CharField(max_length=50, verbose_name="태그")

    class Meta:
        db_table = "content_tag"
        verbose_name = "콘텐츠 태그"
        verbose_name_plural = verbose_name
