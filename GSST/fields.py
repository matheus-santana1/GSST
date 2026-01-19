from django.db import models
from django.db.models.fields.files import FieldFile
from django.urls import reverse


class SecureFieldFile(FieldFile):
    @property
    def url(self):
        if not self.instance.pk:
            return super().url
        return reverse('acessar_arquivo', args=[self.instance.pk])


class SecureFileField(models.FileField):
    attr_class = SecureFieldFile
