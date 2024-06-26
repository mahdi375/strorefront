from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TagItemManager(models.Manager):
    def get_tags_for(self, model, model_id):
        content_type = ContentType.objects.get_for_model(model)

        return TaggedItem.objects \
            .select_related('tag') \
            .filter(content_type=content_type, object_id=model_id)


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label


class TaggedItem(models.Model):
    objects = TagItemManager()

    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
