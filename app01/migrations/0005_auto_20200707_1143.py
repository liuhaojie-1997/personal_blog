# Generated by Django 3.0.4 on 2020-07-07 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_hobby_userinfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Hobby',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
