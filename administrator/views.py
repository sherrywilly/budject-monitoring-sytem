from django.views.generic.list import MultipleObjectMixin
from userapp.models import Expense
from django.contrib.auth.models import User
from django.forms.widgets import DateTimeBaseInput
from django.views.generic.edit import UpdateView
from administrator.forms import BudgetForm, DepartmentForm, HeadForm, createUserForm
from administrator.models import Budget, Department, Head
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView,DetailView
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from django.contrib.auth.decorators import login_required
from administrator.dacorators import adminonly
from django.utils.decorators import method_decorator

# Create your views here.
decorator =[login_required,adminonly]

@method_decorator(decorator,name='dispatch')
class DepartmentCreate(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "index.html"
    success_url = reverse_lazy('dep')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = "create department"
        return context

@method_decorator(decorator,name='dispatch')
class DepartmentList(ListView):
    model = Department
    context_object_name = 'data'
    template_name = "departmentlist.html"

@method_decorator(decorator,name='dispatch')
class DepartmentUpdate(UpdateView):
    model = Department
    form_class = DepartmentForm
    success_url = reverse_lazy('dep')
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = "update department"
        return context



class DepartmentDetailView(DetailView):
    model = Department
    template_name = "departmentdetail.html"
    # slug_url_kwarg ='slug'
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        expamount =[]
        expdate =[]
 
        x =Expense.objects.filter(department__name__icontains=self.kwargs.get('slug'))[:5]
        print(x)
        for i in x:
            expamount.append(i.amount)
            expdate.append(i.date)
        print(expamount)
        print(expdate)
        return context
        
    def get_object(self ):
        slug_ = self.kwargs.get('slug')
        return get_object_or_404(Department,slug=slug_)
    




@login_required
@adminonly
def DepDelete(request, pk):
    if request.method == "POST":
        Department.objects.get(id=pk).delete()
        return redirect('dep')

@method_decorator(decorator,name='dispatch')
class BudgetCreate(CreateView):
    model = Budget
    form_class = BudgetForm
    success_url = reverse_lazy('budlist')
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = "budget create"
        return context

    def form_valid(self, form, *args, **kwargs):
        # updating the  the amount to the balance
        Department.objects.filter(name__iexact=form.cleaned_data.get(
            'department')).update(balance=F('balance')+form.cleaned_data.get('amount'))

        print(form.cleaned_data.get('department'))
        return super().form_valid(form, *args, **kwargs)

@method_decorator(decorator,name='dispatch')
class BudgetList(ListView):
    model = Budget
    context_object_name = 'data'
    template_name = 'budgetlist.html'

@method_decorator(decorator,name='dispatch')
class HeadView(View):
    form1 = createUserForm()
    form2 = HeadForm()

    def get(self, *args, **kwargs):

        context = {
            'form1': self.form1,
            'form2': self.form2
        }
        return render(self.request, "headform.html", context)

    def post(self, *args, **kwargs):
        uForm = createUserForm(self.request.POST)
        hForm = HeadForm(self.request.POST)
        if uForm.is_valid() and hForm.is_valid():
            user = uForm.save()
            user.save()
            head = hForm.save(commit=False)
            head.user = user
            head.groups = 'user'
            head.save()
            return HttpResponseRedirect(reverse_lazy('headlist'))
        else:
            print()
            return HttpResponse(uForm.errors)

@login_required
@adminonly
def HeadDelete(request, pk):
    if request.method == "POST":
        Head.objects.get(id=pk).delete()
        return redirect('headlist')


"""class HeadCreate(CreateView):
    model = Head
    form_class = HeadForm
    success_url = reverse_lazy('headlist')
    template_name = 'headform.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['userForm'] = createUserForm
        context['headForm'] = HeadForm
        return context

    def form_valid(self, form):
        
        return super().form_valid(form)"""

@method_decorator(decorator,name='dispatch')
class HeadList(ListView):
    model = Head
    context_object_name = 'data'
    template_name = 'departmenthead.html'

@method_decorator(decorator,name='dispatch')
class HeadUpdate(UpdateView):
    model = Head
    form_class = HeadForm
    success_url = reverse_lazy('headlist')
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = "department Head Update" 
        return context

@method_decorator(decorator,name='dispatch')
class UserList(ListView):
    model = User
    context_object_name = 'data'
    template_name ="user.html"

@login_required
@adminonly
def userDelete(request,pk):
    if request.method =="POST":
        User.objects.get(id=pk).delete()
        return redirect('userlist')
    
@method_decorator(decorator,name='dispatch')
class AdminDashView(View):
    def get(self,request):
        return render(request,"dashboard.html")