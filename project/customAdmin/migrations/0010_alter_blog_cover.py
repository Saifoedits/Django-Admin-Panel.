# Generated by Django 3.2.12 on 2023-08-17 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customAdmin', '0009_alter_blog_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
