from django.db import models


class Node(models.Model):

    name = models.CharField(max_length=32, null=False, blank=False, unique=True)
    memory = models.IntegerField(null=False, default=1)
    cpu = models.IntegerField(null=False, default=1)
    username = models.CharField(max_length=32, null=False, blank=False)
    password = models.CharField(max_length=32, null=False, blank=False)

    status = models.CharField(max_length=32, null=False, blank=False, default='')

