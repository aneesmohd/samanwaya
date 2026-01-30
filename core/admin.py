from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account, Transaction, Note

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff')
    list_filter = ('role', 'is_approved', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'is_approved')}),
    )

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'account', 'amount', 'transaction_type', 'date', 'performed_by')
    list_filter = ('account', 'transaction_type', 'date')

class NoteAdmin(admin.ModelAdmin):
    list_display = ('account', 'author', 'created_at')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Account)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Note, NoteAdmin)
