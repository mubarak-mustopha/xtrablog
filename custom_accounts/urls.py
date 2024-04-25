from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("manage_account/", views.ManageAccountView.as_view(), name="manage_account"),
    path("edit_profile/", views.UserEditView.as_view(), name="edit_user"),
]
