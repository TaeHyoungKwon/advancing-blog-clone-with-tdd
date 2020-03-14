from django.contrib.contenttypes.models import ContentType

from comments.models import Comment


def get_or_create_new_comment(form, request):
    new_comment, created = Comment.objects.get_or_create(
        user=request.user,
        content_type=ContentType.objects.get(model=form.cleaned_data["content_type"]),
        object_id=form.cleaned_data["object_id"],
        content=form.cleaned_data["content"],
    )
    if created and request.POST.get('parent_id'):
        new_comment.set_parent(int(request.POST.get('parent_id')))
    return new_comment
