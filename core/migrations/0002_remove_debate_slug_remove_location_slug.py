# Generated by Django 5.0.7 on 2024-08-14 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="debate",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="location",
            name="slug",
        ),
    ]
