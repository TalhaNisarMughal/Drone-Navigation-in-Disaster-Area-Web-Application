from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def dronemain(request):
    return render(request,'droneintegration/drone.html')