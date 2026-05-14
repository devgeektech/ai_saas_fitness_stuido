from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth import get_user_model

# Create your models here.
class User(AbstractUser):
 
    ROLE_CHOICES = (
        ('superadmin',   'Super Admin'),
        ('studio_admin', 'Studio Admin'),
        ('trainer',      'Trainer'),
        ('viewer',       'Viewer'),
    )
 
    uuid       = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email      = models.EmailField(unique=True, max_length=100, db_index=True)
    username   = models.CharField(max_length=150, unique=False, db_index=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name  = models.CharField(max_length=50, null=True, blank=True)
    image      = models.ImageField(upload_to='users/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='studio_admin', db_index=True)
    created_by = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='created_users')
    is_active      = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    studio = models.ForeignKey("studio.Studio",on_delete=models.CASCADE,null=True,blank=True)
 
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']
 
    def save(self, *args, **kwargs):
        self.username = self.username.replace(" ", "").lower()
        self.role = self.role.lower()
        super().save(*args, **kwargs)