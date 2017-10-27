from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^travelplan/travels$', views.travels),
    url(r'^travelplan/register$', views.register),
    url(r'^travelplan/login$', views.login),
    url(r'^travelplan/logout$', views.logout),
    url(r'^travelplan/home$', views.home),
    url(r'^travelplan/travels/add$', views.travelsadd),
    url(r'^travelplan/add/trip$', views.addtrip),
    url(r'^travelplan/join/(?P<trip_id>\d+)$', views.jointrip),
    url(r'^travelplan/destination/(?P<trip_id>\d+)$', views.destination),
]
