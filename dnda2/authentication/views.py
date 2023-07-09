from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from . forms import Signup
from . loginform import loginform
from django.contrib.auth import authenticate , logout
from django.contrib.auth import login as u_login
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.path as mpath
import networkx as nx
import joblib
from math import radians,tan
# Create your views here.
def authen(request):
    suc=False
    if request.method == "POST":
        fm=Signup(request.POST)
        if fm.is_valid():
            fm.save()
            suc=True
            fm=Signup()
        else:
            suc="p"
    else:
        fm=Signup()
    return render(request,'auth.html',{"form":fm,"sc":suc})
def login(request):
    if request.method=="POST":
        fm=loginform(request=request , data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            if user is not None:
                u_login(request,user)
                return HttpResponseRedirect("/dashboard/")
    else:
        fm=loginform()
    return render(request, "login.html",{"form":fm})

def imagemap(request):
    return render (request,"imagemap.html")
def imagemap2(request):
    return render (request,"person.html")

    