from django.db import models
from django.contrib.auth.models import User


class Date(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    now = models.DateField()

    class Meta:
        ordering = ['-now']

    def __str__(self) -> str:
        return self.now.strftime("%d-%m-%Y")



class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    date = models.ForeignKey(Date, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['completed', '-updated']
