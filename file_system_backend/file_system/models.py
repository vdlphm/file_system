from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Folder(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(blank=False, max_length=10000, unique=True)
    name = models.CharField(blank=False, max_length=50)
    directory = models.ForeignKey('self', null=True, on_delete=CASCADE)
    create_at =models.DateTimeField()

    def __str__(self):
        return self.path

    class Meta:
        db_table = 'folder'

class File(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(blank=False, max_length=10000, unique=True)
    name = models.CharField(blank=False, max_length=50)
    directory = models.ForeignKey(Folder, on_delete=CASCADE)
    data = models.CharField(max_length=10000)
    create_at =models.DateTimeField()

    def __str__(self):
        return self.path

    class Meta:
        db_table = 'file'