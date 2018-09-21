from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.log_reg),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^notes$', views.notes),
    url(r'^post_note$', views.post_note),
    url(r'^(?P<id>\d+)/read$', views.read),
    url(r'^(?P<id>\d+)/update$', views.update),
    url(r'^(?P<id>\d+)/edit$', views.edit),
    url(r'^(?P<id>\d+)/destroy$', views.destroy),
    url(r'^logout$', views.logout),
    url(r'^api$', views.api),
    url(r'^all.json$', views.all_json),
    url(r'^all.notes$', views.all_notes),
    url(r'^red.notes$', views.red_notes),
    url(r'^blue.notes$', views.blue_notes),
    url(r'^green.notes$', views.green_notes),
    url(r'^yellow.notes$', views.yellow_notes),

]                           