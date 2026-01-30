from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('account/<int:pk>/', views.AccountDetailView.as_view(), name='account_detail'),
    path('account/<int:pk>/pdf/', views.AccountStatementPDFView.as_view(), name='account_pdf'),

    path('transaction/add/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('account/<int:pk>/note/add/', views.NoteCreateView.as_view(), name='note_create'),
]
