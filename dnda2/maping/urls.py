from django.urls import path
from . import views
# from googlemaps import views as googlemaps_views
app_name = 'maping'
urlpatterns=[
    # path("",views.VideoUpload,name="VideoUpload"),
    path("maping/",views.frame_extractor,name="frame_extractor")
]