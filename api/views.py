from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from posts.models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer, CommentListSerializer, CommentCreateSerializer, UserCreateSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwner
from django.db.models import Q
from rest_framework.filters import OrderingFilter, SearchFilter
from django_comments.models import Comment 
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response


class UserLoginView(APIView):
	serializer_class = UserLoginSerializer
	permission_classes = [AllowAny]

	def post(self,request, format=None):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data=serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserCreateView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer

class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializer
	permission_classes = [AllowAny]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['title', 'content', 'author__first_name']

	def get_queryset(self, *args, **kwargs):
		queryset_list = Post.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(author__first_name__icontains=query)|
				Q(author__last_name__icontains=query)
				).distinct()
		return queryset_list

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	permission_classes = [AllowAny]

	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	permission_classes = [IsAuthenticated, IsAdminUser]
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'

class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateSerializer
	permission_classes = [IsAuthenticated, IsAdminUser]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateSerializer
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'

class CommentListView(ListAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentListSerializer
	permission_classes = [AllowAny]

	def get_queryset(self, *args, **kwargs):
		queryset = Comment.objects.all()
		query = self.request.GET.get("q")
		querystr = self.request.GET.get("qs")
		if query:
			if querystr:
				queryset = queryset.filter(
				Q(object_pk=query)|
				Q(user=query)|
				Q(comment__icontains=querystr)
				).distinct()
			else:
				queryset = queryset.filter(
				Q(object_pk=query)|
				Q(user=query)
				).distinct()

		else:
			if querystr:
				queryset = queryset.filter(
				Q(comment__icontains=querystr)
				).distinct()
			
		return queryset

class CommentCreateView(CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentCreateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self,serializer):
		serializer.save(
			content_type=ContentType.objects.get_for_model(Post),
			site=Site.objects.get(id=1),
			user=self.request.user,
			user_name=self.request.user.username,
			submit_date=timezone.now()
			)










