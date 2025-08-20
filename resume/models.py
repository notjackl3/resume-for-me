from django.db import models

class MinorExperience(models.Model):
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)
    included = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} at {self.organisation}"

class Description(models.Model):
    experience = models.ForeignKey(
        MinorExperience,
        on_delete=models.CASCADE,
        related_name="description"
    )
    content = models.TextField()
