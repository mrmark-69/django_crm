from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("homepage:home")
        else:
            return redirect('registration:login')
    else:
        return render(request, 'registration/login.html')


def logout_user(request):
    logout(request)
    return redirect('homepage:home')
