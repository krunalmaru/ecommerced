# Generated by Django 4.1.4 on 2022-12-16 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='link',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
