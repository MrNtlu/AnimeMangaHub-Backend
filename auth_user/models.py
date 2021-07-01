from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
def upload_location(instance, filename, **kwargs):
	file_path = 'profile/{user_id}-{filename}.jpg'.format(
			user_id = str(instance.id),
            filename = str(filename)
		) 
	return file_path


class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, name, password=None):
        if not email:
            raise ValueError("Email shouldn't be empty.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, name=name)
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, None, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):        
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to=upload_location)
    gender = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    about = models.CharField(max_length=1250, blank=True, null=True)
    isPremium = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    

    objects = UserProfileManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return str(self.id) + ' ' + self.email + ' ' + self.username
    
#Login
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
        