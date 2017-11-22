from django.conf.urls import url
from posts import views

urlpatterns = [
    url(r'^home/$', views.post_home, name='home'),
    url(r'^top/$', views.main_post, name='top'),
    url(r'^funny/$', views.fun, name='fun'),
    url(r'^list/$', views.post_list, name = 'list'),
    url(r'^detail/(?P<post_slug>[-\w]+)/$', views.post_detail, name = 'detail'),
    url(r'^create/$', views.post_create, name = 'create'),
    url(r'^update/(?P<post_slug>[-\w]+)/$', views.post_update, name = 'update'),
    url(r'^delete/(?P<post_slug>[-\w]+)/$', views.post_delete, name = 'delete'),
    url(r'^like_button/(?P<post_id>[\d]+)/$', views.like_button, name = 'like_button'),
    url(r'^signup/$', views.usersignup, name = 'signup'),
    url(r'^login/$', views.userlogin, name = 'login'),
    url(r'^logout/$', views.userlogout, name = 'logout'),
]
