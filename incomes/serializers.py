from rest_framework import serializers

from .models import IncomeItem


class IncomeItemSerializer(serializers.ModelSerializer):
    category_title = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = IncomeItem
        fields = ['user', 'id', 'title', 'amount', 'category', 'category_title', 'notes', 'created']

    def get_category_title(self, obj):
        return obj.category.title