from django.shortcuts import render, HttpResponse
from . import models


def home(request):
    #el = models.Goods_daily_stat.objects.get(good_code=121)
    return render (request, "home.html")

def daily_stat(request):
    stats = models.Goods_daily_stat.objects.all()
    return render (request, "goods_daily_stat.html", {"goods_daily_stat": stats})
