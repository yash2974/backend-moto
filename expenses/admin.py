from django.contrib import admin

# Register your models here.
from .models import Expense
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'amount', 'date', 'category', 'description', 'created_at', 'updated_at')
    list_filter = ('category', 'date')
    search_fields = ('description',)

