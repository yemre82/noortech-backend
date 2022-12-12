from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import qrcode
from django.core.files import File
from PIL import Image, ImageDraw
from io import BytesIO

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(blank=False, max_length=30, unique=True)
    created_at = models.DateTimeField(
        verbose_name="created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="update at", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username


    
class Devices(models.Model):
    client_id=models.IntegerField(blank=False)
    pub_id=models.IntegerField(blank=False)
    sub_id=models.IntegerField(blank=False)
    code=models.ImageField(upload_to='code',blank=True)

    def __str__(self):
        return str(self.client_id)
    
    def save(self, *args, **kwargs):
        qr_image = qrcode.make({
            'client_id':self.client_id,
            'pub_id':self.pub_id,
            'sub_id':self.sub_id
        })
        qr_offset = Image.new('RGB',(512,512),'white')
        qr_offset.paste(qr_image)
        files_name=f'{self.id}qr.png'
        stream=BytesIO()
        qr_offset.save(stream,'PNG')
        self.code.save(files_name,File(stream),save=False)
        qr_offset.close()
        super().save(*args, **kwargs)