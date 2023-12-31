# Generated by Django 4.2.7 on 2023-12-02 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study_platform', '0004_remove_course_num_lessons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payed_course_or_lesson',
        ),
        migrations.AddField(
            model_name='payment',
            name='paid_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course', to='study_platform.course'),
        ),
        migrations.AddField(
            model_name='payment',
            name='paid_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='study_platform.subject'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='study_platform.course'),
        ),
    ]
