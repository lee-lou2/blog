# Generated by Django 5.0.7 on 2024-08-07 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0007_alter_contentcomment_parent_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contenttag",
            old_name="tag",
            new_name="name",
        ),
    ]
