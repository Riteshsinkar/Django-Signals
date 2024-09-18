import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Signal receiver
@receiver(post_save, sender=User)
def user_created_signal(sender, instance, **kwargs):
    print(f"Signal thread: {threading.current_thread().name}")

# Trigger the signal
def create_user():
    print(f"Main thread: {threading.current_thread().name}")
    User.objects.create(username="test_user")

create_user()
