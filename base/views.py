from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import PostForm

# Create your views here.


class HomePageView(View):
    def get(self, request):
        return render(request, "home.html", {"active": "home"})


@method_decorator(login_required, name="dispatch")
class CreatePostView(View):
    form_class = PostForm

    def get(self, request):
        form = self.form_class()
        return render(request, "post_form.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post successfully created.")
            return redirect("home")
        return render(request, "post_form.html", {"form": form})
