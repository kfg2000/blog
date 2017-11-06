from django.conf.urls import url
from posts import views

urlpatterns = [
    url(r'^home/$', views.post_home, name='home'),
    url(r'^top/$', views.main_post, name='top'),
    url(r'^funny/$', views.fun, name='fun'),
    url(r'^list/$', views.post_list, name = 'list'),
    url(r'^detail/(?P<post_id>\d+)$', views.post_detail, name = 'detail'),
]
