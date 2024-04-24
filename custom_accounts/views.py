from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm

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
