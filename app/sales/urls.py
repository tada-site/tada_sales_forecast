from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('daily_stat/', views.daily_stat, name="daily_stat"),
]
