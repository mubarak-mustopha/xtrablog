from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("create-post/", views.CreatePostView.as_view(), name="create-post"),
    path("<str:pk>/<slug:slug>/", views.PostView.as_view(), name="post"),
]
