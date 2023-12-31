# Generated by Django 4.2.7 on 2023-12-15 06:24

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0010_alter_profile_image_alter_profile_profilebackground'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=85, scale=None, size=[600, 600], upload_to='profilepics/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profilebackground',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=70, scale=None, size=[1200, 1200], upload_to='profilepics/'),
        ),
    ]
