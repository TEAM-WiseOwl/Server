from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # User 객체 생성 시 연결된 Profile 생성
        Profile.objects.create(user=instance)