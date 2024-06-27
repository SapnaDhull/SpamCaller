# your_app/management/commands/populate_dummy_data.py
# import os
# import random
# from django.core.management.base import BaseCommand
# from faker import Faker
# from api.models import User, Contact, Spam

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spam_detector.settings')  # Replace 'your_project' with your project name
# import django
# django.setup()

# fake = Faker()

# class Command(BaseCommand):
#     help = 'Populate the database with dummy data'

#     def handle(self):
#         self.create_users(10)
#         self.create_contacts(50)
#         self.create_spam_entries(20)
#         self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))

#     def create_users(self, count):
#         for _ in range(count):
#             username = fake.user_name()
#             password = 'password123'  # Use a common password for simplicity
#             phone_number = fake.phone_number()
#             email = fake.email()
#             user = User.objects.create_user(username=username, password=password, phone_number=phone_number, email=email)
#             self.stdout.write(f'Created user: {username}')

#     def create_contacts(self, count):
#         users = list(User.objects.all())
#         for _ in range(count):
#             user = random.choice(users)
#             name = fake.name()
#             phone_number = fake.phone_number()
#             email = fake.email() if random.choice([True, False]) else ''
#             contact = Contact.objects.create(user=user, name=name, phone_number=phone_number, email=email)
#             self.stdout.write(f'Created contact for user {user.username}: {name}, {phone_number}')

#     def create_spam_entries(self, count):
#         for _ in range(count):
#             phone_number = fake.phone_number()
#             spam = Spam.objects.create(phone_number=phone_number, count=random.randint(1, 10))
#             self.stdout.write(f'Created spam entry: {phone_number}')

import os
import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import User, Contact, Spam

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spam_detector.settings')
import django
django.setup()

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **options):
        self.create_users(20)
        self.create_contacts(20)
        self.create_spam_entries(20)
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))

    def create_users(self, count):
        for _ in range(count):
            username = fake.user_name()
            password = 'password123'
            phone_number = self.generate_valid_phone_number()
            email = fake.email()
            user = User.objects.create_user(username=username, password=password, phone_number=phone_number, email=email)
            self.stdout.write(f'Created user: {username}')

    def create_contacts(self, count):
        users = list(User.objects.all())
        for _ in range(count):
            user = random.choice(users)
            name = fake.name()
            phone_number = self.generate_valid_phone_number()
            email = fake.email() if random.choice([True, False]) else ''
            contact = Contact.objects.create(user=user, name=name, phone_number=phone_number, email=email)
            self.stdout.write(f'Created contact for user {user.username}: {name}, {phone_number}')

    def create_spam_entries(self, count):
        for _ in range(count):
            phone_number = self.generate_valid_phone_number()
            spam = Spam.objects.create(phone_number=phone_number, count=random.randint(1, 10))
            self.stdout.write(f'Created spam entry: {phone_number}')

    def generate_valid_phone_number(self):
        phone_number = fake.phone_number()
        return phone_number[:15]  # Truncate to 15 characters to ensure it fits in the database
