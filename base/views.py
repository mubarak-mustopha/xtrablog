from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Post, Tag
from .forms import PostForm, CommentForm, PostUpdateForm
from .utils import add_post_tags, remove_post_tags

# Create your views here.


class HomePageView(View):
    def get(self, request):
        query = request.GET.get("query")

        if query == None or query.strip() == "":
            posts = Post.objects.all()
        else:
            conditionals = (
                Q(title__icontains=query)
                | Q(user__username__icontains=query)
                | Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
            )
            try:
                tag = Tag.objects.get(name__icontains=query)
                conditionals = conditionals | Q(tags=tag)
            except Tag.DoesNotExist:
                pass
            posts = Post.objects.filter(conditionals).distinct()
            messages.success(request, f"Showing {posts.count()} results for '{query}'")

        paginator = Paginator(posts, 4)
        page = request.GET.get("page")
        current_page = paginator.get_page(page)
        previous_page_number = (
            current_page.previous_page_number() if current_page.has_previous() else None
        )
        next_page_number = (
            current_page.next_page_number() if current_page.has_next() else None
        )

        return render(
            request,
            "home.html",
            {
                "active": "home",
                "current_page": current_page,
                "page_range": paginator.page_range,
                "previous_page_number": previous_page_number,
                "next_page_number": next_page_number,
            },
        )


@method_decorator(login_required, name="dispatch")
class CreatePostView(View):
    form_class = PostForm
    context = {"title": "Create"}

    def get(self, request):
        form = self.form_class()
        self.context.update({"form": form})
        return render(request, "post_form.html", self.context)

    def post(self, request):
        form = self.form_class(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            tags = form.cleaned_data["tags"]
            post.save()
            add_post_tags(post, tags)
            post.save()
            messages.success(request, "Post successfully created.")
            return redirect(post)
        self.context.update({"form": form})
        return render(request, "post_form.html", self.context)


@method_decorator(login_required, name="dispatch")
class UpdatePostView(View):
    form_class = PostUpdateForm
    context = {"title": "Update"}

    def get(self, request, pk, slug):
        post = Post.objects.get(id=pk, slug=slug)
        tag_names = post.tags.values_list("name", flat=True)
        initial_tags = ", ".join(tag_names)
        form = self.form_class(
            instance=post,
            initial={
                "tags": initial_tags,
                "initial_tags": initial_tags,
            },
        )
        self.context["form"] = form
        return render(request, "post_form.html", self.context)

    def post(self, request, pk, slug):
        post = Post.objects.get(id=pk, slug=slug)
        form = self.form_class(request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            updated_tags = form.cleaned_data["tags"]
            initial_tags = form.cleaned_data["initial_tags"]
            removed_tags = set(initial_tags).difference(updated_tags)
            added_tags = set(updated_tags).difference(initial_tags)
            add_post_tags(post, added_tags)
            remove_post_tags(post, removed_tags)
            messages.success(request, "Post successfully updated.")
            return redirect(post)
        else:
            self.context["form"] = form
            return render(request, "post_form.html", self.context)


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
