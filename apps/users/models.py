import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email=email, username=username, password=password, **extra_fields)
    
# Custom Usermodel
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # def get_full_name(self):
    #     return self.full_name
    
    # def get_short_name(self):
    #     """Returns the first name or full name is no spaces exist."""
    #     return self.full_name.split(" ")[0] if " " in self.full_name else self.full_name

    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name="profile")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.first_name + ' ' + self.last_name
        return super().save(*args, **kwargs)
    