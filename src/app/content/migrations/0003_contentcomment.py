# Generated by Django 5.0.7 on 2024-08-06 03:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0002_author_content_author"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ContentComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.CharField(max_length=255, verbose_name="내용")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="생성일시"),
                ),
                (
                    "content",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="content_comments",
                        to="content.content",
                        verbose_name="콘텐츠",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="content_comments",
                        to="content.contentcomment",
                        verbose_name="부모 댓글",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="content_comments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="��용자",
                    ),
                ),
            ],
            options={
                "verbose_name": "콘텐츠 댓글",
                "verbose_name_plural": "콘텐츠 댓글",
                "db_table": "content_comment",
            },
        ),
    ]
