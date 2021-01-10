from userapp.views import ExpenseCreate, ExpenseUpdate, ExpenseView
from django.urls import  path

urlpatterns = [
    path('expense/create',ExpenseCreate.as_view(),name="expensecreate"),
    path('expense/',ExpenseView.as_view(),name="expenselist"),
    path('expense/<int:pk>/update/',ExpenseUpdate,name="expenseupdate")
]
