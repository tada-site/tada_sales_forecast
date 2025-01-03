from django.shortcuts import render
from django.db import connections
from . import models

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

        return render (request, "test.html", 
                       {"departments": departments, "dep_id": dep_id, "dep_name": dep_name})
    else:
        departments = models.Departments.objects.all()
        return render (request, "test.html", {"departments": departments})


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

        return render (request, "goods.html", 
                       {"goods": goods, "good_code": good_code, "good_name":
                        good_name})
    else:
        goods = models.Goods.objects.all()
        return render (request, "goods.html", {"goods": goods})


def good(request, uuid):
    good = models.Goods.objects.get(pk=uuid)
    return render (request, "one_good.html", {"good": good})


def categories(request):
    if request.method == "POST":
        cat_name = request.POST['cat_name']
        categories = models.Categories.objects.filter(name_ua__icontains=cat_name)

        return render (request, "categories.html", 
                       {"categories": categories, "good_name": cat_name})
    else:
        categories = models.Categories.objects.all()
        return render (request, "categories.html", {"categories": categories})


def category(request, uuid):
    category = models.Categories.objects.get(pk=uuid)
    return render (request, "one_category.html", {"category": category})
