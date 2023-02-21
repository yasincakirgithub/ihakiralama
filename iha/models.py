from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid

class IHACategory(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class IHA(models.Model):
    creator = models.ForeignKey(User,models.CASCADE)
    mark = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    weight = models.FloatField(default=0,null=True,blank=True)
    category = models.ForeignKey(IHACategory,models.CASCADE,null=True,blank=True)
    slug = models.CharField(max_length=32,null=True,blank=True)
    status = models.BooleanField(default=True)
    date_of_record = models.DateTimeField(null=True,blank=True)
    date_of_update = models.DateTimeField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4()).replace("-","")
        if not self.date_of_record:
            self.date_of_record = datetime.now()
        self.date_of_update = datetime.now()
        super(IHA, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.creator.username}-{self.mark}-{self.model}-{self.weight}"
