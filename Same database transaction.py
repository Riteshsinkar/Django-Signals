from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import connection

# Signal receiver
@receiver(post_save, sender=User)
def user_created_signal(sender, instance, **kwargs):
    print(f"Signal: User with username {instance.username} created")

# Trigger the signal
def create_user_with_transaction():
    try:
        with transaction.atomic():
            print("Creating user")
            user = User.objects.create(username="test_user")
            print("User created, raising exception to rollback")
            raise Exception("Rollback transaction")
    except Exception as e:
        print(f"Exception: {e}")

    # Check if the user was created in the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM auth_user WHERE username = 'test_user'")
        row = cursor.fetchone()
        if row:
            print("User found in database")
        else:
            print("User not found in database")

create_user_with_transaction()
