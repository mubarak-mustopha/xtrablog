from django.shortcuts import render
from django.views import View
from .forms import PostForm

# Create your views here.


class HomePageView(View):
    def get(self, request):
        return render(request, "home.html", {"active": "home"})


class CreatePostView(View):
    form_class = PostForm

    def get(self, request):
        form = self.form_class()
        return render(request, "post_form.html", {"form": form})

    def post(self, request):
        pass
