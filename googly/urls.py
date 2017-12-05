from django.conf.urls import url
from posts import views
from googly import views

urlpatterns = [
    url(r'^place/search/$', views.place_text_search, name='place-search'),
    url(r'^place/detail/$', views.place_detail, name='place-detail'),
]