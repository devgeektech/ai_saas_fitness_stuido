from django.db import models
from authentication.models import User
import uuid

# Create your models here.
class Studio(models.Model):
    uuid        = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name        = models.CharField(max_length=200, null=True, blank=True)
    slug        = models.SlugField(unique=True, null=True, blank=True)
    logo        = models.ImageField(upload_to='studios/', null=True, blank=True)
    brand_color = models.CharField(max_length=50, null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'studios'
        
        
# exercises
class Exercise(models.Model):

    DIFFICULTY_CHOICES = (
        ('beginner',     'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced',     'Advanced'),
    )

    STATUS_CHOICES = (
        ('draft',    'Draft'),
        ('approved', 'Approved'),
    )

    uuid         = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name         = models.CharField(max_length=200, null=True, blank=True)
    category     = models.CharField(max_length=100, null=True, blank=True)
    difficulty   = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, null=True, blank=True)
    muscle_group = models.CharField(max_length=100, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    safety_notes = models.TextField(null=True, blank=True)
    demo_video   = models.FileField(upload_to='exercises/videos/', null=True, blank=True)
    thumbnail    = models.ImageField(upload_to='exercises/thumbnails/', null=True, blank=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'studio_exercises'
    
        
# classes
class Class(models.Model):

    DIFFICULTY_CHOICES = (
        ('beginner',     'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced',     'Advanced'),
    )

    STATUS_CHOICES = (
        ('draft',      'Draft'),
        ('generating', 'Generating'),
        ('ready',      'Ready'),
        ('failed',     'Failed'),
    )

    uuid       = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    studio     = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='classes')
    title      = models.CharField(max_length=200, null=True, blank=True)
    category   = models.CharField(max_length=100, null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, null=True, blank=True)
    focus      = models.CharField(max_length=100, null=True, blank=True)
    duration   = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='classes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'studio_classes'