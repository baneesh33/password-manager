# Generated by Django 3.2.8 on 2021-10-14 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('password_manager', '0004_rename_sharedpasswords_sharedpasswordsdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedpasswordsdetails',
            name='date',
        ),
    ]
