from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name="test"),
    path('test/<int:dep_id>/', views.testId, name="test"),
    path('', views.goods, name="goods"),
    path('goods/', views.goods, name="goods"),
    path('good/<str:uuid>/', views.good, name="good"),
    path('categories/', views.categories, name="categories"),
    path('category/<str:uuid>/', views.category, name="category"),
]
