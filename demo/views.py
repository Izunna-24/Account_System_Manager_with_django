from django.shortcuts import render, HttpResponse


# Create your views here.
# localhost:8080/demo/hello

def say_hello(request):
    return HttpResponse("Welcome to Django Demo! ")


def welcome(request, name):
    return render(request, "index.html", {"name": name})
