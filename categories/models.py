from django.db import models

from accounts.models import User


class Category(models.Model):

    class CategoryType(models.TextChoices):
        EXPENSE = 'E', "Expense"
        INCOME = 'I', "Income"

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=120)
    type = models.CharField(max_length=1, choices=CategoryType.choices)
    is_automated = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title