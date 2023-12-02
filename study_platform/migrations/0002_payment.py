# Generated by Django 4.2.7 on 2023-11-28 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study_platform', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_day', models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')),
                ('payed_course_or_lesson', models.CharField(max_length=100, verbose_name='Оплаченный курс или урок')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Сумма оплаты')),
                ('payment_method', models.CharField(choices=[('cash', 'Наличные'), ('card', 'Банковская карта')], max_length=10, verbose_name='Способ оплаты')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
                'ordering': ['-pay_day'],
            },
        ),
    ]
