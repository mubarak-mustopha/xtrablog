from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("create-post/", views.CreatePostView.as_view(), name="create-post"),
    path("<uuid:pk>/<slug:slug>/", views.PostView.as_view(), name="post"),
    path(
        "update/<uuid:pk>/<slug:slug>/",
        views.UpdatePostView.as_view(),
        name="update-post",
    ),
]
