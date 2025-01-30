from django.db import models
from django.utils.text import slugify
from .choices import STATUS_CHOICES

class Blog(models.Model):
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    read_count = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  
    date = models.DateTimeField(auto_now_add=True) 
    page_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    display = models.BooleanField(default=True)
    content = models.TextField()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.page_name)  
        super().save(*args, **kwargs)
    def __str__(self):
        return self.page_name

    class Meta:
        ordering = ['-date']  
