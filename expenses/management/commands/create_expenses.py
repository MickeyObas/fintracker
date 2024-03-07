from django.core.management.base import BaseCommand

from expenses.models import ExpenseItem
from categories.models import Category
from accounts.models import User

import random

class Command(BaseCommand):
    help = 'Creates a bunch of expenses'

    def handle(self, *args, **kwargs):
        user = User.objects.get(email='admin@email.com')
        random_title = ''
        words = ['tom', 'hank', 'blah', 'frek', 'herye', 'rgrw']
        for i in range(10):
            random_title += random.choice(words)
            random_title += " "
        for i in range(50):
            random_number = random.choice(
                Category.objects.filter(user=user).values('id')
            ).get('id')
            ExpenseItem.objects.create(
                user=user,
                title=random_title,
                amount = random.randint(1, 10000),
                category=Category.objects.get(id=random_number)
            )
        self.stdout.write(self.style.SUCCESS(f'Expenses for {user} created successfully!'))