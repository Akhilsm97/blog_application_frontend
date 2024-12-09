from django.db import models
from django.utils.text import slugify

# Create your models here.

class Post(models.Model):
    post_name = models.CharField(max_length=200)
    post_slug  = models.SlugField(max_length=30,blank=True)
    blog_preview  = models.TextField()
    blog_content = models.TextField()
    category = models.CharField(max_length=200)
    blog_image   = models.ImageField(upload_to='Post/')
    Status = models.CharField(max_length=200)
    visibility = models.CharField(max_length=200)
    Comments = models.CharField(max_length=200)
    updated_by = models.CharField( max_length=200, blank=True)
    author_name = models.CharField(max_length=200)
    author_id = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.post_slug:
            self.post_slug = slugify(self.post_name)  # Auto-generate the slug from title
        super().save(*args, **kwargs)
    

class UsersDetails(models.Model):
    Name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=15, blank=True, null=True)

    # String representation
    def __str__(self):
        return f"{self.username}'s Details"
    

class Comment(models.Model):
    # Relationship fields
    user = models.IntegerField()
    post = models.IntegerField()

    # Comment content
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author_name = models.CharField(max_length=200)

    # String representation
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

    class Meta:
        ordering = ['-created_at']  # Newest comments first

class Login(models.Model):
    username = models.CharField(max_length=200)    
    password = models.CharField(max_length=200)      