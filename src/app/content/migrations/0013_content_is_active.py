# Generated by Django 5.0.7 on 2024-08-13 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0012_contentreport"),
    ]

    operations = [
        migrations.AddField(
            model_name="content",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="활성 상태"),
        ),
    ]
