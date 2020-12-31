from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.expressions import OrderBy
from django.shortcuts import reverse
from django.core.validators import MinValueValidator


# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)
    balance = models.FloatField(blank=True, null=True, validators=[MinValueValidator(
        0.00, message="you dont have enough budget to raise fund")], default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_update_url(self):
        return reverse("depupdate", kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Head(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, models.CASCADE)
    join_date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_update_url(self):
        return reverse('headupdate',kwargs={'pk':self.pk})

    class Meta:
        unique_together = ('user','department')

    def __str__(self):
        return str(self.user)


class Budget(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    amount = models.FloatField(
        validators=[MinValueValidator(0.00, message="you should enter a valid amount")])
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering= ['-date']

    @property
    def balance(self):
        obj = self.department.objects.get(id=self.department)
        return obj

    @property
    def fdate(self):
        return self.date.strftime('%d-%m-%Y')