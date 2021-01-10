from django.db.models import F
from django.http.response import HttpResponse
from administrator.models import Department
from django.urls.base import reverse, reverse_lazy
from django.views.generic.list import ListView
from userapp.forms import ExpenseForm
from userapp.models import Expense
from django.shortcuts import redirect, render
from django.views.generic import View, CreateView
from django.contrib.auth.models import User
import copy
from typing import Final
# Create your views here.


class ExpenseCreate(CreateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy('expensecreate')
    template_name = "user/form.html"

    def form_valid(self, form):

        form.user = 1
        return super().form_valid(form)


class ExpenseView(View):
    def get(self, request, *args, **kwargs):
        try:
            data = Expense.objects.filter(
                department=User.objects.get(id=2).head.department)
        except:
            data = ''
        context = {
            'data': data
        }
        return render(request, 'user/expense.html', context)


def ExpenseUpdate(request, pk):
    obj_data = Expense.objects.get(id=pk)
    a: Final = obj_data.amount
    print(f"{a} is instance")
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=obj_data)
        if form.is_valid():
            obj = form.save(commit=False)
            x = obj.amount
            print(f"{x} is the input")
            sum = a-x
            sumx=-sum
            Department.objects.filter(name__iexact=obj.department).update(balance=F('balance')-sumx)
            obj.save()
            return redirect(reverse('expenselist'))
         
            
        
        # if x < a:
        #     print("a is greater than x")
        #     sum = x-a
        #     x=Department.objects.get(name__iexact=obj.department)
        #     x.update(balance=F('balance')+sum)
        #     print(x)
    
        # elif x > a:
        #     sum = x-a
        #     print(sum)
        #     print("x is greater than  a")
        # else:
        #     print("those are equal")
    context = {
        'form': ExpenseForm(instance=obj_data)
    }
    return render(request, 'user/form.html', context)
