from django.db import models

from config import settings
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='previews/', verbose_name='Превью', **NULLABLE)
    price = models.IntegerField(verbose_name='Цена', default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    objects = models.Manager()

    def __str__(self):
        return f'{self.title}, {self.price}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title']


class Subject(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='previews/', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField()
    price = models.IntegerField(verbose_name='Цена', default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, related_name='lessons')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['title']


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='владелец')
    objects = models.Manager()
    pay_day = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, related_name='course')
    paid_lesson = models.ForeignKey(Subject, on_delete=models.CASCADE, **NULLABLE, related_name='lesson')
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method_choices = [
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
    ]
    payment_method = models.CharField(max_length=10, choices=payment_method_choices, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user} paid for {self.paid_course if self.paid_course else self.paid_lesson}: {self.pay_day}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-pay_day']


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE, related_name='subs')
    subscription = models.BooleanField(default=False, verbose_name='Подписка')
    objects = models.Manager()

    def __str__(self):
        return f'{self.user} {self.course}: {self.subscription}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
