# Generated by Django 4.2.7 on 2023-11-28 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_platform', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='num_lessons',
            field=models.IntegerField(default=0),
        ),
    ]
