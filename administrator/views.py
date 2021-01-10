from django.contrib.auth.models import User
from django.forms.widgets import DateTimeBaseInput
from django.views.generic.edit import UpdateView
from administrator.forms import BudgetForm, DepartmentForm, HeadForm, createUserForm
from administrator.models import Budget, Department, Head
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import F

# Create your views here.


class DepartmentCreate(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "index.html"
    success_url = reverse_lazy('dep')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = "create department"
        return context


class DepartmentList(ListView):
    model = Department
    context_object_name = 'data'
    template_name = "departmentlist.html"


class DepartmentUpdate(UpdateView):
    model = Department
    form_class = DepartmentForm
    success_url = reverse_lazy('dep')
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = "update department"
        return context


def DepDelete(request, pk):
    if request.method == "POST":
        Department.objects.get(id=pk).delete()
        return redirect('dep')


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


class BudgetList(ListView):
    model = Budget
    context_object_name = 'data'
    template_name = 'budgetlist.html'


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
            head.save()
            return HttpResponseRedirect(reverse_lazy('headlist'))
        else:
            print()
            return HttpResponse(uForm.errors)


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


class HeadList(ListView):
    model = Head
    context_object_name = 'data'
    template_name = 'departmenthead.html'


class HeadUpdate(UpdateView):
    model = Head
    form_class = HeadForm
    success_url = reverse_lazy('headlist')
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = "department Head Update" 
        return context


class UserList(ListView):
    model = User
    context_object_name = 'data'
    template_name ="user.html"


def userDelete(request,pk):
    if request.method =="POST":
        User.objects.get(id=pk).delete()
        return redirect('userlist')
    
class AdminDashView(View):
    def get(self,request):
        return HttpResponse("dashboard")