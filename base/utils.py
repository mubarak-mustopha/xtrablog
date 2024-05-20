from .models import Tag


def add_post_tags(post, tag_names):
    """
    Add tags with labels from tag_labels
    to post object.
    """
    for name in tag_names:
        tag_obj, created = Tag.objects.get_or_create(name=name)
        if created:
            tag_obj.save()
        post.tags.add(tag_obj)


def remove_post_tags(post, tag_names):
    """
    Remove tags with labels from tag_labels
    from post object.
    """
    for name in tag_names:
        tag_obj = Tag.objects.get(name=name)
        post.tags.remove(tag_obj)
