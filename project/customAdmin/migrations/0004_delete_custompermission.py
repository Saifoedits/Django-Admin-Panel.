# Generated by Django 3.2.12 on 2023-08-11 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customAdmin', '0003_custompermission'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomPermission',
        ),
    ]
