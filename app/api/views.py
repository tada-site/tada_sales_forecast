from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import connections
from . import models
from django.contrib.auth.decorators import login_required
from .helpers import GROUP_BY_DAY, GROUP_BY_MONTH, GROUP_BY_YEAR, get_good_graph_data, return_city_graph


items_per_page = 10


def test(request):
    if request.method == "POST":
        dep_id = request.POST['dep_id']
        dep_name = request.POST['dep_name']

        if dep_id != "":
            department = models.Departments.objects.get(pk=dep_id)
            departments = [department]
        else:
            departments = models.Departments.objects.filter(name__icontains=dep_name)

        paginator = Paginator(departments, items_per_page) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        departments = page_obj.object_list

        return render (request, "test.html", 
                       {"departments": departments, "dep_id": dep_id, "dep_name": dep_name})
    else:
        departments = models.Departments.objects.all()

        paginator = Paginator(departments, items_per_page) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        departments = page_obj.object_list

        graph = return_city_graph()
        
        return render (request, "test.html", {"departments": departments, "page_obj": page_obj, 
                                              'graph': graph})


def testId(request, dep_id):
    department = models.Departments.objects.get(pk=dep_id)

    cursor = connections['test_db'].cursor()
    cursor.execute('select count(*) as c from departments where name like \
        "%відділення%"')
    res = cursor.fetchone()
    print(res)

    return render (request, "one_test.html", {"department": department})


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
