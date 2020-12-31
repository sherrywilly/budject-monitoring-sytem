from django.db import models
from django.db.models.fields import DateTimeField
from administrator.models import Department
from django.contrib.auth.models import User
from datetime import  datetime
from django.db.models import F
# Create your models here.

class Expense(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-timestamp"]

    @property
    def balance(self):
        return self.department.balance

    def __str__(self):
        return self.name


    def save(self,*args, **kwargs):
        x=Department.objects.filter(name__iexact=self.department)
        print(x)
        x.update(balance=F('balance')-self.amount)
        return super().save(*args, **kwargs)