from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='api_user_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='api_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='api_user_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='api_user',
    )

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class Spam(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.phone_number} - {self.count}"
































# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models

# class User(AbstractUser):
#     phone_number = models.CharField(max_length=15, unique=True)
#     email = models.EmailField(blank=True, null=True)
    
#     groups = models.ManyToManyField(
#         Group,
#         related_name='api_user_set',  # Custom related name
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         related_query_name='api_user',
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='api_user_set',  # Custom related name
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_query_name='api_user',
#     )

# class Contact(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
#     name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=15)
#     email = models.EmailField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.name} - {self.phone_number}"

# class Spam(models.Model):
#     phone_number = models.CharField(max_length=15, unique=True)
#     count = models.IntegerField(default=1)

#     def __str__(self):
#         return f"{self.phone_number} - {self.count}"
