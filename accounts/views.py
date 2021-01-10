from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
# Create your views here.


class Loginview(View):
    def get(self,request):
        return render(request,'accounts/login.html')
    
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get("password")
        print(f'{username} and {password}')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            print(request.user)
        else:
            return HttpResponse('invalid user')
            
        return HttpResponse("test")
        # return HttpResponseRedirect(reverse_lazy(''))
        
        

def logout_view(request):
    logout(request)
    return redirect('loginpage')