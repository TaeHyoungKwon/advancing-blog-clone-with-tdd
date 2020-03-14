from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from trydjango19.helpers import get_or_create_new_comment

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Comment


def comment_thread(request, id):
    try:
        obj = Comment.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404

    if not obj.is_parent:
        obj = obj.parent

    initial_data = {"content_type": obj.content_type, "object_id": obj.object_id}
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        new_comment = get_or_create_new_comment(form, request)
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {"comment": obj, "form": form}
    return render(request, "comment_thread.html", context)

@login_required
def comment_delete(request, id):
    try:
        obj = Comment.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404

    if obj.user != request.user:
        return HttpResponse(status=403, content="you do not have permission")

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    return render(request, "confirm_delete.html", {"object": obj})
