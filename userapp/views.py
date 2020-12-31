from django.urls.base import reverse_lazy
from django.views.generic.list import ListView
from userapp.forms import ExpenseForm
from userapp.models import Expense
from django.shortcuts import render
from django.views.generic import View,CreateView
from django.contrib.auth.models import User
# Create your views here.


class ExpenseCreate(CreateView):
    model = Expense
    form_class = ExpenseForm
    success_url = reverse_lazy('expensecreate')
    template_name ="user/form.html"


    def form_valid(self, form):
        
        form.user = 1
        return super().form_valid(form)

class ExpenseList(ListView):
    model= Expense
    context_object_name ="data"
    template_name =''