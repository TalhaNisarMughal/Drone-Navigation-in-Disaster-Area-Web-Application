from django.urls import path,include
from . import views
from pathplanning import views as v_p
urlpatterns=[
    path("",views.dashboard),
    path("pp/", v_p.pathplanning,name="pathplanning"),
    path("ppNFZ/", v_p.pathplanning_NFZ,name="pathplanningNFZ"),
    # path("video-upload/",include('maping.urls'))
    path("video-upload/",views.VideoUpload,name="VideoUpload")
    
]