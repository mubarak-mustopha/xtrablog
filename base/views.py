from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Post, Tag
from .forms import PostForm, CommentForm
from .utils import add_post_tags

# Create your views here.


class HomePageView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home.html", {"active": "home", "posts": posts})


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
            tags = form.cleaned_data["tags"].split(",")
            post.save()
            add_post_tags(post, tags)
            post.save()
            messages.success(request, "Post successfully created.")
            return redirect(post)
        return render(request, "post_form.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class UpdatePostView(View):
    form_class = PostForm

    def get(self, request, pk, slug):
        post = Post.objects.get(id=pk, slug=slug)
        form = self.form_class(instance=post)
        tag_names = post.tags.values_list("name", flat=True)
        form.fields["tags"].initial = ", ".join(tag_names)
        return render(request, "post_form.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class PostView(View):
    def get(self, request, pk, slug):
        post = Post.objects.get(id=pk, slug=slug)
        comments = post.comments.all()
        form = CommentForm()
        context = {
            "post": post,
            "comments": comments,
            "form": form,
        }
        return render(request, "post.html", context)

    def post(self, request, pk, slug):
        post = Post.objects.get(id=pk, slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
        return redirect(post)
