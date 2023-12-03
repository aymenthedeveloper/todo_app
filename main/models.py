from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} completed={self.completed}"

    class Meta:
        ordering = ['completed', '-updated']
