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
    is_active = models.BooleanField(verbose_name="활성 상태", default=True)
    image_url = models.URLField(verbose_name="이미지 URL", blank=True, default="")
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)
    created_at = models.DateTimeField(verbose_name="생성일시", auto_now_add=True)
    like_count = models.IntegerField(verbose_name="좋아요 수", default=0)
    view_count = models.IntegerField(verbose_name="조회 수", default=0)

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
        verbose_name="사용자",
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
    name = models.CharField(max_length=50, verbose_name="태그")

    class Meta:
        db_table = "content_tag"
        verbose_name = "콘텐츠 태그"
        verbose_name_plural = verbose_name


class ContentLike(models.Model):
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name="content_likes",
        verbose_name="콘텐츠",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="content_likes",
        verbose_name="사용자",
    )
    is_like = models.BooleanField(verbose_name="좋아요 여부", default=True)
    created_at = models.DateTimeField(verbose_name="생성일시", auto_now_add=True)

    class Meta:
        db_table = "content_like"
        verbose_name = "콘텐츠 좋아요"
        verbose_name_plural = verbose_name


class ContentReport(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="content_reports",
        verbose_name="사용자",
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name="content_reports",
        verbose_name="콘텐츠",
    )
    message = models.TextField(verbose_name="신고 내용")
    created_at = models.DateTimeField(verbose_name="생성일시", auto_now_add=True)

    class Meta:
        db_table = "content_report"
        verbose_name = "콘텐츠 신고"
        verbose_name_plural = verbose_name
