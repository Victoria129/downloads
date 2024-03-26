from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, null=True)
    link_clicks = models.IntegerField(default=0)
    filename = models.CharField(max_length=1000,blank=True)
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=("groups"),
        blank=True,
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=("user permissions"),
        blank=True,
        related_name="customuser_set",  # Unique related_name for user_permissions
        related_query_name="user",
    )

    def __str__(self):
        return self.username
    
    def check_clicks(self):
        if self.link_clicks > 0:
            return True
        return False
    
class Logs(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    filename = models.CharField(max_length=1000)
