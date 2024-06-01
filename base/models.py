import uuid
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(null=False, upload_to="posts/")
    description = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    created = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ["-created", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"pk": self.id, "slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    description = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.body[:50]
