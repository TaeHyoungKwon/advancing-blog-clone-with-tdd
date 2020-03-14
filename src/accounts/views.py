from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm, UserRegisterForm


def login_view(request):
    next_ = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next_:
            return redirect(next_)
        return redirect("/posts")
    return render(request, "form.html", {"form": form, "title": "Login"})


def register_view(request):
    next_ = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next_:
            return redirect(next_)
        return redirect('/')
    return render(request, "form.html", {"form": form, "title": "Register"})


def logout_view(request):
    logout(request)
    return render(request, "form.html", {})
