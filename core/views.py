from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Account, Transaction, Note
from .forms import TransactionForm, NoteForm
from .utils import render_to_pdf


class IsOfficerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_officer()


class CustomLoginView(LoginView):
    template_name = 'core/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')


class DashboardView(ListView):
    model = Account
    template_name = 'core/dashboard.html'
    context_object_name = 'accounts'


class AccountDetailView(DetailView):
    model = Account
    template_name = 'core/account_detail.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['transactions'] = (
            self.object.transactions
            .select_related('performed_by')
            .order_by('-date', '-created_at')
        )

        context['notes'] = (
            self.object.notes
            .select_related('author')
            .order_by('-created_at')
        )

        credits = self.object.transactions.filter(transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        debits = self.object.transactions.filter(transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_income'] = credits
        context['total_expense'] = debits

        if self.request.user.is_authenticated and self.request.user.is_officer():
            context['transaction_form'] = TransactionForm(
                initial={'account': self.object}
            )
        else:
            context['transaction_form'] = None

        context['note_form'] = NoteForm() if self.request.user.is_authenticated else None

        return context


class AccountStatementPDFView(DetailView):
    model = Account

    def get(self, request, *args, **kwargs):
        account = self.get_object()
        transactions = (
            account.transactions
            .select_related('performed_by')
            .order_by('-date', '-created_at')
        )

        credits = account.transactions.filter(transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        debits = account.transactions.filter(transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0

        context = {
            'account': account,
            'transactions': transactions,
            'total_income': credits,
            'total_expense': debits,
        }
        return render_to_pdf('core/account_pdf.html', context)


class TransactionCreateView(LoginRequiredMixin, IsOfficerMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'core/transaction_form.html'

    def form_valid(self, form):
        form.instance.performed_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'account_detail',
            kwargs={'pk': self.object.account.pk}
        )


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.account = get_object_or_404(
            Account, pk=self.kwargs['pk']
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'account_detail',
            kwargs={'pk': self.object.account.pk}
        )
