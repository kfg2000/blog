from django.conf.urls import url
from api.views import *

urlpatterns = [
	url(r'^list/$', PostListAPIView.as_view(), name="list"),
	url(r'^detail/(?P<post_slug>[-\w]+)/$', PostDetailAPIView.as_view(), name="detail"),
	url(r'^delete/(?P<post_slug>[-\w]+)/$', PostDeleteAPIView.as_view(), name="delete"),
	url(r'^update/(?P<post_slug>[-\w]+)/$', PostUpdateAPIView.as_view(), name="update"),
	url(r'^create/$', PostCreateAPIView.as_view(), name="create"),
	url(r'^comments/$', CommentListView.as_view(), name="comment-list"),
	url(r'^comments/create/$', CommentCreateView.as_view(), name="comment-create"),
	url(r'^register$', UserCreateView.as_view(), name="register"),
	url(r'^login$', UserLoginView.as_view(), name="login"),

]