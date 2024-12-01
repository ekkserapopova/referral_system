from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class NewUserManager(BaseUserManager):
    def create_user(self, phone_number):
        if not phone_number:
            raise ValueError('The phone number is required')
        user = self.model(phone_number=phone_number, username=phone_number)
        user.save(using=self._db)
        return user
    
    
class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=12, unique=True)
    invited_code = models.CharField(max_length=6, unique=True, null=True)
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL,null=True)
    
    is_active = models.BooleanField(default=True)
    objects =  NewUserManager()
    USERNAME_FIELD='phone_number'
    class Meta:
        db_table = 'users'
    
class VerificationCodes(models.Model):
    phone = models.CharField(max_length=12, unique=True)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_created=datetime.now())
    
    class Meta:
        db_table = 'verification_codes'