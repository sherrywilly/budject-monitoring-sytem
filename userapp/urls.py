from userapp.views import ExpenseCreate
from django.urls import  path

urlpatterns = [
    path('expense/create',ExpenseCreate.as_view(),name="expensecreate")
]
