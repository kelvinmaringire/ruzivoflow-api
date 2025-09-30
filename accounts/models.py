from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from wagtail.images.models import Image


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    cell_no = models.CharField(max_length=17, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='Physical address')
    sex = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(verbose_name='Date of birth', null=True, blank=True)
    pic = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_query_name='user_pic')
    company_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ExtendedUser.objects.create(user=instance)    

