# Generated by Django 3.1 on 2021-01-21 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cgpa',
            field=models.CharField(default='NA', max_length=6),
        ),
    ]