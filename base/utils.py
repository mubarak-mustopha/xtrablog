from .models import Tag


def add_post_tags(post, tag_labels):
    """
    Add tags with labels from tag_labels
    to post object.
    """
    for label in tag_labels:
        label = label.strip().capitalize()
        if not label:  # if label is an empty string.
            continue
        tag_obj, created = Tag.objects.get_or_create(name=label)
        if created:
            tag_obj.save()
        post.tags.add(tag_obj)
