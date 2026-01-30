import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samanwaya.settings')
django.setup()

from core.models import User, Account, Transaction, Note
from django.test import Client

def run_checks():
    print("Setting up test users...")
    User.objects.all().delete()
    Account.objects.all().delete()
    
    officer = User.objects.create_user(username='pres', password='password123', role='president', is_approved=True)
    member = User.objects.create_user(username='mem', password='password123', role='member', is_approved=True)
    unapproved = User.objects.create_user(username='new', password='password123', role='member', is_approved=False)
    
    print("Creating Account...")
    acc = Account.objects.create(name='General Fund', description='Main club fund', account_type='club')
    
    c = Client()
    
    print("\n--- TEST 1: Unapproved User ---")
    c.login(username='new', password='password123')
    resp = c.get('/', follow=True) 
    # Logic: Login -> Dashboard -> Check Perm -> Redirect Unapproved
    # The CustomLoginView redirects to Unapproved if not approved.
    # So we expect to land on /unapproved/
    if 'unapproved' in str(resp.request['PATH_INFO']):
        print("PASS: Unapproved user redirected to unapproved page.")
    else:
        print(f"FAIL: User landed on {resp.request['PATH_INFO']}")
        
    c.logout()

    print("\n--- TEST 2: Approved Member Access ---")
    c.login(username='mem', password='password123')
    resp = c.get('/')
    if resp.status_code == 200:
        print("PASS: Approved member accessed Dashboard.")
    else:
        print(f"FAIL: Member got {resp.status_code}")

    print("\n--- TEST 3: Officer Transaction ---")
    c.login(username='pres', password='password123')
    resp = c.post('/transaction/add/', {
        'account': acc.pk,
        'amount': 100.00,
        'transaction_type': 'credit',
        'description': 'Donation',
        'date': '2025-01-01'
    })
    
    if resp.status_code == 302:
        print("PASS: Officer added transaction.")
    elif resp.status_code == 200:
        print(f"FAIL: Officer Transaction Form errors: {resp.context['form'].errors}")
    else:
        print(f"FAIL: Status {resp.status_code}")

    print("\n--- TEST 4: Member Transaction Restricted ---")
    c.login(username='mem', password='password123')
    resp = c.post('/transaction/add/', {
        'account': acc.pk,
        'amount': 500.00,
        'transaction_type': 'debit',
        'description': 'Theft'
    })
    if resp.status_code == 403:
        print("PASS: Member denied transaction (403).")
    else:
        print(f"FAIL: Member got {resp.status_code} (Expected 403)")

    print("\n--- TEST 5: Member Note ---")
    resp = c.post(f'/account/{acc.pk}/note/add/', {'text': 'Hello world'})
    if resp.status_code == 302:
        print("PASS: Member added note.")
    else:
        print(f"FAIL: Member failed to add note. {resp.status_code}")

    print("\n--- TEST 6: Balance Check ---")
    acc.refresh_from_db()
    print(f"Final Balance: {acc.balance}")
    if acc.balance == 100.00:
        print("PASS: Balance calculation correct.")
    else:
        print(f"FAIL: Balance is {acc.balance}, expected 100.00")

if __name__ == '__main__':
    run_checks()
