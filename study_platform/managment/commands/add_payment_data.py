from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from study_platform.models import Payment


class Command(BaseCommand):
    help = 'Записывает данные в модель "Платежи"'

    def handle(self, *args, **options):
        user = User.objects.get(username='user1')
        payment = Payment.objects.create(user=user, date='2023-11-28', course_or_lesson='Python for Data Science',
                                         amount=100.00, payment_method='cash')
        payment.save()
        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены в модель "Платежи"'))
