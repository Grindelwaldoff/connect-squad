from django.db import models
from django.conf import settings
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def deduct_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            self.record_payment('deduction', amount)
            return True
        return False

    def increase_balance(self, amount):
        self.balance += amount
        self.save()
        self.record_payment('increase', amount)

    def record_payment(self, method, amount):
        user = self.user
        payment = Payment.objects.create(
            user=user,
            method=method,
            amount=amount,
            status='completed',
            created_at=timezone.now(),
            paid_at=timezone.now()
        )
        return payment


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    payment_id = models.AutoField(primary_key=True)
    method = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.payment_id)
