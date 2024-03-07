from django.core.management import BaseCommand

from accounts.models import User
from categories.models import Category
from ...models import IncomeItem

import random


class Command(BaseCommand):

    help = 'Create a bunch of income objects'

    def handle(self, *args, **kwargs):
        user = User.objects.get(email='admin@email.com')
        random_title = ''
        words = ['tom', 'hank', 'blah', 'frek', 'herye', 'rgrw']
        for i in range(10):
            random_title += random.choice(words)
            random_title += " "
        for i in range(50):
            IncomeItem.objects.create(
                user=user,
                title=random_title,
                amount = random.randint(1, 10000),
                category=Category.objects.get(id=4)
            )
        self.stdout.write(self.style.SUCCESS(f'Incomes for {user} created successfully!'))

        