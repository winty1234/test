from django.db import models


from  django.contrib.auth.models import  AbstractUser



class User(AbstractUser):
    full_name = models.CharField(max_length=128, blank=False, null=False)
    phone = models.CharField(max_length=21, blank=False, null=False, verbose_name="Телефон")
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Users"
        db_table = "user"


class Application(models.Model):
    class Transport(models.TextChoices):
        BUS = "bus", "Автобус"
        TROLLEY = "trolley", "Электробус"
        TRAM = "tram", "Трамвай"

    class PaymentType(models.TextChoices):
        CARD = "card", "картой"
        CASH = "cash", "наличными"

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "Идет обучение"
        END = "end", "Обучение завершено"

    time_start = models.DateField(null=True, blank=True)
    transport = models.CharField(choices=Transport.choices, max_length=20, default=Transport.BUS)
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, default=PaymentType.CARD)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.NEW)

    def __str__(self):
        return f"{self.user} - {self.transport}"


class Review(models.Model):
    content = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.application}"