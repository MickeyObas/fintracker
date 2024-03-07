from .models import ExpenseItem

from rest_framework import serializers


class ExpenseItemSerializer(serializers.ModelSerializer):
    category_title = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseItem
        fields = [
            "id",
            "user",
            "title",
            "amount",
            "category_title",
            "notes",
            "created_date",
        ]

    def get_category_title(self, obj):
        return obj.category.title if obj.category else None

    def get_created_date(self, obj):
        return obj.created.strftime("%d-%m-%y")
