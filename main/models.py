from django.db import models


class Date(models.Model):
    now = models.DateField()

    class Meta:
        ordering = ['-now']

    def __str__(self) -> str:
        return self.now.strftime("%d-%m-%Y")

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    date = models.ForeignKey(Date, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.name} completed={self.completed}"

    class Meta:
        ordering = ['completed', '-updated']
