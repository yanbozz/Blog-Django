# Generated by Django 2.2.2 on 2019-08-08 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
