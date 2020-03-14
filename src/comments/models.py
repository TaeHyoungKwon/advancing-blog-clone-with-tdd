from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models


class CommentManager(models.Manager):
    def all(self):
        return super().filter(parent=None)

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return super().filter(content_type=content_type, object_id=instance.id).filter(parent=None)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    parent = models.ForeignKey("self", null=True, blank=True)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        return False if self.parent else True

    def set_parent(self, parent_id):
        parent_qs = Comment.objects.filter(id=parent_id)
        if parent_qs.count() == 1:
            self.parent = parent_qs.first()
            self.save()
