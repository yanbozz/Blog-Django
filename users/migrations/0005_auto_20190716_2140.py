# Generated by Django 2.2.2 on 2019-07-16 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190715_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
