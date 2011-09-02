from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User)
    emailaddress = models.EmailField()
    content = models.CharField(max_length = 140)
    time1 = models.DateTimeField()#(input_formats = '%Y-%m-%dD%H:-%M:-%S:T')