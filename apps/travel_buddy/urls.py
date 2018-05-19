from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^process$', views.process, name='process'),
	url(r'^login$', views.login, name='login'),
	url(r'^dashboard$', views.dashboard, name='home'),
	url(r'^add_plan$', views.add_plan, name='make_plan'),
	url(r'^make_plan$', views.make_plan, name='make_plan'),
	url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
	url(r'^join/(?P<id>\d+)$', views.join, name='join'),
	url(r'^clear$', views.clear, name='clear'),
]