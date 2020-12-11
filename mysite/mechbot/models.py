from django.db import models
from .managers import DiscordUserOauth2Manager
from django.forms import ModelForm

# Create your models here.
class DiscordUser(models.Model):
    objects = DiscordUserOauth2Manager()

    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    public_flags = models.IntegerField()
    flags = models.IntegerField()
    locale = models.CharField(max_length=100)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)
    email = models.CharField(max_length=320)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + " " + str(self.username)
    def has_perm(self, perm, obj=None):
       return self.is_superuser
    def has_module_perms(self, app_label):
       return self.is_superuser
    def is_authenticated(self, request):
        return True
    def get_username(self):
        return self.username
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Alert(TimeStampMixin):
    user_id = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)
    has = models.CharField(max_length=50,null=True,blank=True)
    wants = models.CharField(max_length=50,null=True,blank=True)
    origin = models.CharField(max_length=7,null=True,blank=True)
    hit_counter = models.IntegerField(default=0) # How many times this notification actually caught something
    enabled =  models.BooleanField(default=True)
    #Target is always DMs bc im lazy to make server channels lol


