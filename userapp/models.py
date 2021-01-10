from django.db import models
from django.db.models.fields import DateTimeField
from administrator.models import Department
from django.contrib.auth.models import User
from datetime import  datetime
from django.db.models import F
from django.core.validators import MinValueValidator
# Create your models here.

class Expense(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0.00,message="amount should be greater than 0")])
    timestamp = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-timestamp"]

    @property
    def balance(self):
        return self.department.balance

    def __str__(self):
        return self.name


    # def save(self,instance,*args, **kwargs):
    #     print('self.save()')
    #     # x=Department.objects.filter(name__iexact=self.department)
    #     # x.update(balance=F('balance')-self.amount)
    #     if self.instance is not None:
    #         print("update")
    #         return super().save(instance,*args,**kwargs)
    #     return super().save(*args, **kwargs)


 