# Generated by Django 2.2.7 on 2020-03-25 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20200325_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aspirant',
            name='blockchain_address',
        ),
    ]
