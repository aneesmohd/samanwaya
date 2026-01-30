from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('president', 'President'),
        ('treasurer', 'Treasurer'),
        ('secretary', 'Secretary'),
        ('member', 'Member'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    is_approved = models.BooleanField(default=False, help_text="Designates whether this user has been approved by an officer.")

    def is_officer(self):
        return self.role in ['admin', 'president', 'treasurer', 'secretary'] or self.is_superuser

class Account(models.Model):
    TYPE_CHOICES = (
        ('club', 'Club Account'),
        ('event', 'Event Account'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    account_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='club')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def balance(self):
        credits = self.transactions.filter(transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        debits = self.transactions.filter(transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        return credits - debits

class Transaction(models.Model):
    TYPE_CHOICES = (
        ('credit', 'Credit (Income)'),
        ('debit', 'Debit (Expense)'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

class Note(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.author} on {self.account}"
