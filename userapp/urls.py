from userapp.views import BudgetView, ExpenseCreate, ExpenseUpdate, ExpenseView, UserDashboard
from django.urls import  path

urlpatterns = [
    path('expense/create',ExpenseCreate.as_view(),name="expensecreate"),
    path('expense/',ExpenseView.as_view(),name="expenselist"),
    path('expense/<int:pk>/update/',ExpenseUpdate,name="expenseupdate") ,
    path('dashboard/',UserDashboard.as_view(),name="userdashboard")  ,
    path('budget/',BudgetView.as_view(),name="budget")  
]
