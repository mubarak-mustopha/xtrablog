from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import CustomUserCreationForm, UserEditForm

# Create your views here.


class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "registration/signup.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(request, "registration/signup.html", {"form": form})


class UserEditView(View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, "registration/user_edit_form.html", {"form": form})

    def post(self, request):
        form = UserEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully updated!")
            return redirect("manage_account")
        else:
            return render(request, "registration/user_edit_form.html", {"form": form})


class ManageAccountView(View):
    def get(self, request):
        return render(request, "manage_account.html", {"active": "manage_account"})
