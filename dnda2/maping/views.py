from django.shortcuts import render

# Create your views here.
def frame_extractor(request):
    if request.method =='POST':
        return("Path Recieved")
