from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("create-post/", views.CreatePostView.as_view(), name="create-post"),
]
