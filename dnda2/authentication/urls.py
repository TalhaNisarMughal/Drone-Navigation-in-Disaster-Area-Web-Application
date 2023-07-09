from django.urls import path,include
from . import views 
# from dashboard import views as dashboard_views
urlpatterns = [
    path('', views.login,name="login"),
    path("signup/",views.authen, name='signup'),
    path("dashboard/",include('googlemaps.urls')),
    path("dashboard/map",views.imagemap,name='map'),
    path("dashboard/map2",views.imagemap2,name='map2')
]
