from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from . import models


@login_required(login_url="/login/")
def home(request):
    #el = models.Goods_daily_stat.objects.get(good_code=121)
    return render (request, "home.html")

@login_required(login_url="/login/")
def daily_stat(request):
    stats = models.Goods_daily_stat.objects.all()
    return render (request, "goods_daily_stat.html", {"goods_daily_stat": stats})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user=user)

                if "next" in request.POST:
                    return redirect(request.POST.get("next"))
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
