from django.contrib import messages

from trydjango19.helpers import get_or_create_new_comment

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Comment


def comment_thread(request, id):
    obj = get_object_or_404(Comment, id=id)
    initial_data = {"content_type": obj.content_type, "object_id": obj.object_id}
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        new_comment = get_or_create_new_comment(form, request)
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {"comment": obj, "form": form}
    return render(request, "comment_thread.html", context)


def comment_delete(request, id):
    obj = get_object_or_404(Comment, id=id)
    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    return render(request, "confirm_delete.html", {"object": obj})
