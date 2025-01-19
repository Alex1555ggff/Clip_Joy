# Generated by Django 5.1.4 on 2025-01-05 18:28

import django.core.validators
import vlog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vlog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-username']},
        ),
        migrations.RemoveField(
            model_name='user',
            name='subscribers_count',
        ),
        migrations.RemoveField(
            model_name='video',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='video',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='video',
            name='likes',
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=512),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='logo',
            field=models.ImageField(default='channel_images/AnonymUser.png', upload_to='channel_images/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default=vlog.models.generate_unique_name, max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='videos/videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])]),
        ),
    ]
