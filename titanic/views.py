# Create your views here.
from django.http.response import HttpResponse
from rest_framework import viewsets
from titanic.models import Titanic
from titanic.myserializer import TitanicSerializer
from titanic.models import Titanic
from titanic import TiML2
from rest_framework.response import Response

class TitanicViewSet(viewsets.ModelViewSet):
    queryset = Titanic.objects.order_by("-id")
    serializer_class = TitanicSerializer
    def create(self, request, *args, **kwargs):
        viewsets.ModelViewSet.create(self, request, *args, **kwargs)
        ob = Titanic.objects.latest("id")
        sur = TiML2.pred(ob)
        return Response({"status": "Success", "Survived": sur, 'tmp': args})  # Your override
        
        
