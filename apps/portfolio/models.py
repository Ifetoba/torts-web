from django.db import models
from django.db.models import Max

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=500)
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    live_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.order:  # If order is not set
            # Get the maximum order value and add 1
            max_order = Project.objects.aggregate(Max('order'))['order__max']
            self.order = (max_order or 0) + 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order', '-created_at']
