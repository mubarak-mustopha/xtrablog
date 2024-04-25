from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, UserEditForm


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = UserEditForm
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
    ]
