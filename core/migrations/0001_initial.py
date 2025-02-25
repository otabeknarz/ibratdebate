# Generated by Django 5.0.7 on 2025-02-24 10:49

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('telegram_group_link', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
                'indexes': [models.Index(fields=['created_at'], name='core_locati_created_40de8f_idx')],
            },
        ),
        migrations.CreateModel(
            name='Debate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('name_uz', models.CharField(blank=True, max_length=500, null=True)),
                ('name_en', models.CharField(blank=True, max_length=500, null=True)),
                ('name_ru', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('description_uz', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('description_ru', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/news/')),
                ('date', models.DateTimeField()),
                ('is_expired', models.BooleanField(default=False)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='debates', to='core.location')),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('is_used', models.BooleanField(default=False)),
                ('qr_code_path', models.CharField(blank=True, max_length=255, null=True)),
                ('debate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='core.debate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
                'indexes': [models.Index(fields=['created_at'], name='core_ticket_created_fe6f19_idx')],
            },
        ),
    ]
