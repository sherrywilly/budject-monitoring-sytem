from django.db.models import F
from django.http.response import HttpResponse
from administrator.models import Budget, Department
from django.urls.base import reverse, reverse_lazy
from userapp.forms import ExpenseForm
from userapp.models import Expense
from django.shortcuts import redirect, render
from django.views.generic import View, CreateView
from django.contrib.auth.models import User
from typing import Final
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from userapp.dacorators import useronly
# Create your views here.

dacorator =[login_required,useronly]
@method_decorator(dacorator,name='dispatch')
class ExpenseCreate(CreateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy('expensecreate')
    template_name = "user/form.html"
    
    def get_context_data(self, *args,**kwargs) :
        context =super().get_context_data(*args,**kwargs)
        context['head'] = "expense create"
        return context

    def form_valid(self, form):
        try: 
            form.user = self.request.user
        except:
            form.user = 1
        department = form.cleaned_data['department']
        print(department)
        amount = form.cleaned_data['amount']
        x=Department.objects.filter(name__iexact=department)
        x.update(balance=F('balance')-amount)
        return super().form_valid(form)

@method_decorator(dacorator,name='dispatch')
class ExpenseView(View):
    def get(self, request, *args, **kwargs):
        try:
            data = Expense.objects.filter(
                department=request.user.head.department)
        except:
            data = ''
        context = {
            'data': data,
            
        }
        return render(request, 'user/expense.html', context)

@login_required
@useronly
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
            sumx = -sum
            Department.objects.filter(name__iexact=obj.department).update(
                balance=F('balance')-sumx)
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
        'form': ExpenseForm(instance=obj_data),
        'head':"Expense update"
    }
    print(request.user)
    return render(request, 'user/form.html', context)

@method_decorator(dacorator,name='dispatch')
class UserDashboard(View):
    def get(self, *args, **kwargs):
        
        budget =Budget.objects.filter(department=self.request.user.head.department)
        print(budget)
        exp = Expense.objects.filter(department=self.request.user.head.department)
        print(exp)
        context = {
            
        }
        return render(self.request,'user/dashboard.html',context)


@method_decorator(dacorator,name='dispatch')
class BudgetView(View):
    def get(self,request):
        try:
         x=Budget.objects.filter(department=request.user.head.department)
        except:
            x = []
        context={
            'budget':x
        }
        
        return render(request,'user/budget.html',context)
    
    
    