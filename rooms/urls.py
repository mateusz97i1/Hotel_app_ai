from django.urls import path
from . import views

app_name='rooms'

urlpatterns = [
    path('', views.home, name='home'),
    path('availability',views.check_room_availability, name='room_availability')
]

