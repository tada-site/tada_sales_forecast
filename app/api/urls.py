from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_stat, name="all_stat"),
    path('goods/', views.goods, name="goods"),
    path('good/<str:uuid>/', views.good, name="good"),
    path('categories/', views.categories, name="categories"),
    path('category/<str:uuid>/', views.category, name="category"),
]
