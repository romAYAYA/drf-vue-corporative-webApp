# Generated by Django 5.0.4 on 2024-05-19 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("django_app", "0007_profile_timezone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="timezone",
        ),
    ]