from django.db import models

# Create your models here.

class blog(models.Model):
    cover = models.ImageField(upload_to='images/', null=True, blank=True)
    title = models.CharField(max_length=1000)
    content = models.TextField()
    slug = models.SlugField(unique=True, null=True)
    tag = models.CharField(max_length=300)
    category = models.CharField(max_length=300, default='uncategorized')


class category(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey(
    "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
