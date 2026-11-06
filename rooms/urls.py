from django.urls import path
from . import views

app_name='rooms'

urlpatterns = [
    path('', views.home, name='home'),
    path('availability',views.check_room_availability, name='room_availability'),
    path('booking/<uuid:room_id>/',views.booking_page, name='booking'),
    path('create_profile',views.create_profile_guest,name='create_profile')
]

