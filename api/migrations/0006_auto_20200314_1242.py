# Generated by Django 2.2.7 on 2020-03-14 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_voter_password_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='password_salt',
            field=models.CharField(max_length=255),
        ),
    ]