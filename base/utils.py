from .models import Tag


def add_post_tags(post, tag_labels):
    """
    Add tags with labels from tag_labels 
    to post object.
    """
    for tag in tag_labels:
        tag = tag.strip().capitalize()
        tag_obj, created = Tag.objects.get_or_create(name=tag)
        if created:
            tag_obj.save()
        post.tags.add(tag_obj)
