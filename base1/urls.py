from django.urls import path, include
from base1.views import NearestComp

urlpatterns = [
    path('nearest-store/', NearestComp.as_view() )
]