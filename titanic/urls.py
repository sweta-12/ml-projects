from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from titanic import views
from django.views.generic.base import RedirectView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'titanic', views.TitanicViewSet)
 
urlpatterns = [
    path(r'api/', include(router.urls)),    
    path('', RedirectView.as_view(url="api/")),
]

