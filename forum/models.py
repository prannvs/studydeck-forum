from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True) 
    title = models.CharField(max_length=200) 
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code}: {self.title}"

class Resource(models.Model):
    RESOURCE_TYPES = [('PDF', 'PDF'), ('VIDEO', 'Video'), ('LINK', 'Link')]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    link = models.URLField()

    def __str__(self):
        return self.title
    


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Thread(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads')
    course_tag = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    likes = models.ManyToManyField(User, related_name='thread_likes', blank=True)

    def total_likes(self):
        return self.likes.count()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            while Thread.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{str(uuid.uuid4())[:4]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.thread.title}"