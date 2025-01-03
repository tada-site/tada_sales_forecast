from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import connections
import calendar
from time import gmtime, strftime
from datetime import datetime, timedelta
from . import models

items_per_page = 10

# Create your views here.
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
        page_number = request.get.get("page")
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
        
        return render (request, "test.html", {"departments": departments, "page_obj": page_obj})


def testId(request, dep_id):
    department = models.Departments.objects.get(pk=dep_id)

    cursor = connections['test_db'].cursor()
    cursor.execute('select count(*) as c from departments where name like \
        "%відділення%"')
    res = cursor.fetchone()
    print(res)

    return render (request, "one_test.html", {"department": department})


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
        page_number = request.get.get("page")
        page_obj = paginator.get_page(page_number)
        goods = page_obj.object_list

        return render (request, "goods.html", 
                       {"goods": goods, "good_code": good_code, "good_name":
                        good_name, "page_obj": page_obj})
    else:
        goods = models.Goods.objects.all()

        paginator = Paginator(goods, items_per_page) 
        page_number = request.get.get("page")
        page_obj = paginator.get_page(page_number)
        goods = page_obj.object_list

        return render (request, "goods.html", {"goods": goods, "page_obj": page_obj})


def good(request, uuid):
    good = models.Goods.objects.get(pk=uuid)


    date_from = datetime.today().replace(day=1)
    date_from_str = date_from.strftime("%Y-%m-%d")
    last_d = calendar.monthrange(int(strftime("%Y", gmtime())), int(strftime("%m", gmtime())))[1]
    date_to = datetime.today().replace(day=last_d).strftime("%Y-%m-%d")

    last_month_from = (date_from - timedelta(days=date_from.day)).replace(day=1).strftime("%Y-%m-%d")
    last_month_to = (date_from - timedelta(days=date_from.day)).strftime("%Y-%m-%d")

    cursor = connections['test_db'].cursor()
    cursor.execute("select count(*) c from `Order_goods` where order_uuid in (select uuid from Orders \
    where `date` <= '" + date_to +  "' and `date` >= '" + date_from_str + "') and good_code =" + good.good_code)
    res = cursor.fetchone()
    sales_this_month = res[0]

    cursor.execute("select count(*) c from `Order_goods` where order_uuid in (select uuid from Orders \
    where `date` <= '" + last_month_to +  "' and `date` >= '" + last_month_from + "') and good_code =" + good.good_code)
    res = cursor.fetchone()
    sales_last_month = res[0]

    return render (request, "one_good.html", {"good": good, "this_month": sales_this_month, "last_month": sales_last_month})


def categories(request):
    if request.method == "POST":
        cat_name = request.POST['cat_name']
        categories = models.Categories.objects.filter(name_ua__icontains=cat_name)

        paginator = Paginator(categories, items_per_page) 
        page_number = request.get.get("page")
        page_obj = paginator.get_page(page_number)
        categories = page_obj.object_list

        return render (request, "categories.html", 
                       {"categories": categories, "good_name": cat_name, "page_obj": page_obj})
    else:
        categories = models.Categories.objects.all()

        paginator = Paginator(categories, items_per_page) 
        page_number = request.get.get("page")
        page_obj = paginator.get_page(page_number)
        categories = page_obj.object_list

        return render (request, "categories.html", {"categories": categories, "page_obj": page_obj})


def category(request, uuid):
    category = models.Categories.objects.get(pk=uuid)
    return render (request, "one_category.html", {"category": category})
