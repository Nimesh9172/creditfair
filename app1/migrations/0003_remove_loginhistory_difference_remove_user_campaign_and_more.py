# Generated by Django 4.1.7 on 2023-03-22 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_loginhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginhistory',
            name='difference',
        ),
        migrations.RemoveField(
            model_name='user',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='user',
            name='usergroup',
        ),
        migrations.AddField(
            model_name='user',
            name='is_loggedin',
            field=models.CharField(blank=True, default=0, max_length=2, null=True),
        ),
    ]