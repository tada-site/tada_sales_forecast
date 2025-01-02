from django.shortcuts import render
from . import models

# Create your views here.
def test(request):

    if request.method == "POST":
        searched = request.POST['searched']
        departments = models.Departments.objects.filter(name__icontains=searched)
        return render (request, "test.html", 
                       {"departments": departments, "searched": searched})
    else:
        departments = models.Departments.objects.all()
        return render (request, "test.html", {"departments": departments})


def goods(request):
    departments = models.Departments.objects.all()
    return render (request, "departments.html", {"departments": departments})


def categories(request):
    departments = models.Departments.objects.all()
    return render (request, "departments.html", {"departments": departments})
