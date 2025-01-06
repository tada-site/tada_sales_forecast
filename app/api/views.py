from django.shortcuts import render
from django.core.paginator import Paginator
from . import models
from django.contrib.auth.decorators import login_required
from .helpers import GROUP_BY_DAY, GROUP_BY_MONTH, GROUP_BY_YEAR, get_city_graph_data, get_good_graph_data


items_per_page = 10


@login_required(login_url="/login/")
def all_stat(request):
    sales_by_city_month = get_city_graph_data(GROUP_BY_MONTH)
    sales_by_day = get_good_graph_data(0, GROUP_BY_DAY)
    sales_by_month = get_good_graph_data(0, GROUP_BY_MONTH)
    sales_by_year = get_good_graph_data(0, GROUP_BY_YEAR)

    return render (request, "all_stat.html", {"graph_day": sales_by_day,
                                              "graph_month": sales_by_month,
                                              "graph_year": sales_by_year,
                                              "graph_city": sales_by_city_month
                                              })


@login_required(login_url="/login/")
def goods(request):
    if request.method == "POST":
        good_code = request.POST['good_code']
        good_name = request.POST['good_name']

        if good_code != "":
            good = models.Goods.objects.get(good_code=good_code)
            goods = [good]
        else:
            goods = models.Goods.objects.filter(title_ua__icontains=good_name)

        paginator = Paginator(goods, items_per_page) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        goods = page_obj.object_list

        return render (request, "goods.html", 
                       {"goods": goods, "good_code": good_code, "good_name":
                        good_name, "page_obj": page_obj})
    else:
        goods = models.Goods.objects.all()

        paginator = Paginator(goods, items_per_page)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        goods = page_obj.object_list

        return render (request, "goods.html", {"goods": goods, "page_obj": page_obj})


@login_required(login_url="/login/")
def good(request, uuid):
    good = models.Goods.objects.get(pk=uuid)

    sales_by_day = get_good_graph_data(good.good_code, GROUP_BY_DAY)
    sales_by_month = get_good_graph_data(good.good_code, GROUP_BY_MONTH)
    sales_by_year = get_good_graph_data(good.good_code, GROUP_BY_YEAR)
    return render (request, "one_good.html", {"good": good, 
                                              "graph_day": sales_by_day,
                                              "graph_month": sales_by_month,
                                              "graph_year": sales_by_year})


@login_required(login_url="/login/")
def categories(request):
    if request.method == "POST":
        cat_name = request.POST['cat_name']
        categories = models.Categories.objects.filter(name_ua__icontains=cat_name)

        paginator = Paginator(categories, items_per_page)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        categories = page_obj.object_list

        return render (request, "categories.html",
                       {"categories": categories, "good_name": cat_name, "page_obj": page_obj})
    else:
        categories = models.Categories.objects.all()

        paginator = Paginator(categories, items_per_page)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        categories = page_obj.object_list

        return render (request, "categories.html", {"categories": categories, "page_obj": page_obj})


@login_required(login_url="/login/")
def category(request, uuid):
    category = models.Categories.objects.get(pk=uuid)

    sales_by_day = get_good_graph_data(category.uuid, GROUP_BY_DAY, True)
    sales_by_month = get_good_graph_data(category.uuid, GROUP_BY_MONTH, True)
    sales_by_year = get_good_graph_data(category.uuid, GROUP_BY_YEAR, True)

    return render (request, "one_category.html", {"category": category,
                                              "graph_day": sales_by_day,
                                              "graph_month": sales_by_month,
                                              "graph_year": sales_by_year})
