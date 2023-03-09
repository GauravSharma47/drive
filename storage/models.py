from django.db import models
from django.contrib.auth.models import User

class CustomFile(models.Model):
    name = models.CharField(max_length=40)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    file=models.FileField(upload_to='files')
    size=models.IntegerField(default=0)
    createdAt=models.DateTimeField(auto_now_add=True,null=True)
    updatedAt=models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.name


