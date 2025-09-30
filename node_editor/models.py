from django.db import models, transaction
from django.contrib.auth.models import User

from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.documents.models import Document


@register_snippet
class NodeCategory(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    header_class = models.CharField(max_length=20, default="bg-primary")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

    panels = [
        FieldPanel("name"),
        FieldPanel("icon"),
        FieldPanel("description"),
        FieldPanel("header_class")
    ]


@register_snippet
class Node(models.Model):
    name = models.CharField(max_length=15)
    category = models.ForeignKey(NodeCategory, on_delete=models.SET_NULL, null=True)
    html_id = models.CharField(max_length=15)
    type = models.CharField(max_length=20)
    icon = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    order = models.IntegerField()
    show = models.BooleanField(default=True)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
        FieldPanel("category"),
        FieldPanel("html_id"),
        FieldPanel("type"),
        FieldPanel("icon"),
        FieldPanel("order"),
        FieldPanel("show"),
        FieldPanel("disabled")
    ]

    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"
        ordering = ["order", "name"]


@register_snippet
class Workflow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=18)
    description = models.TextField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', '-updated']

    panels = [
        FieldPanel("name"),
        FieldPanel("user"),
        FieldPanel("description")
    ]


@register_snippet
class NodeItem(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    original_name = models.CharField(max_length=15)
    filename = models.CharField(max_length=40, null=True)
    original_id = models.CharField(max_length=15)
    name = models.CharField(max_length=15)
    html_id = models.CharField(max_length=30, unique=True)
    icon = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=20)
    data_type = models.CharField(max_length=20, null=True)
    style_object = models.JSONField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)
    formData = models.JSONField(null=True, blank=True)
    edited = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.html_id})"

    panels = [
        FieldPanel("name")
    ]

    def get_ancestors(self):
        ancestors = []
        node = self
        while node.parent:
            ancestors.append(node.parent)
            node = node.parent
        return ancestors

    def get_descendants(self):
        descendants = []
        nodes_to_check = list(self.children.all())
        while nodes_to_check:
            node = nodes_to_check.pop(0)
            descendants.append(node)
            nodes_to_check.extend(node.children.all())
        return descendants

    def delete(self, *args, **kwargs):
        # Use transaction to ensure all deletions succeed or fail together
        with transaction.atomic():
            # Delete associated connections
            Connection.objects.filter(workflow=self.workflow, sourceId=self.html_id).delete()
            Connection.objects.filter(workflow=self.workflow, targetId=self.html_id).delete()

            # Delete associated documents
            Document.objects.filter(title=self.html_id).delete()

            # Delete the NodeItem itself
            super(NodeItem, self).delete(*args, **kwargs)


@register_snippet
class Connection(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    sourceId = models.CharField(max_length=30)
    targetId = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.sourceId} -> {self.targetId}'

    panels = [
        FieldPanel("workflow"),
        FieldPanel("sourceId"),
        FieldPanel("targetId"),
    ]
