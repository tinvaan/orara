# Generated by Django 2.0.2 on 2019-04-19 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20181107_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='orarauser',
            name='gender',
            field=models.BooleanField(default=True, verbose_name='Gender'),
        ),
    ]
