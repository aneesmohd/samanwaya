# Samanwaya - Club Accounting System

Samanwaya is a Django-based accounting application designed for clubs and organizations to manage their finances effectively. It provides a simple and intuitive interface for tracking accounts, transactions, and generating statements.

## Features

*   **User Management:** Role-based access control for different user types (Admin, President, Treasurer, Secretary, Member).
*   **Account Management:** Create and manage different types of accounts (e.g., Club Account, Event Accounts).
*   **Transaction Tracking:** Record income (credit) and expenses (debit) with detailed descriptions and optional receipts.
*   **Account Statements:** View detailed account statements and export them as PDF files.
*   **Notes:** Add notes to accounts for important information and reminders.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.8+
*   Django 4.0+

### Installation

1.  **Clone the repository:**
    ```bash
<<<<<<< HEAD
    git clone https://github.com/your-username/samanwaya.git
=======
    https://github.com/aneesmohd/samanwaya.git
>>>>>>> d994c5e046e69600c1b709eeea5d9d5775c70309
    cd samanwaya
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`.

## Usage

1.  **Login:** Access the admin panel at `http://127.0.0.1:8000/admin/` with your superuser credentials to manage users and their roles.
2.  **Dashboard:** The main dashboard displays a list of all accounts.
3.  **Account Details:** Click on an account to view its details, including all transactions and notes.
4.  **Add Transactions:** Officers can add new transactions (credit or debit) to an account.
5.  **PDF Statements:** Download a PDF statement for any account.

## Built With

*   [Django](https://www.djangoproject.com/) - The web framework used
*   [Bootstrap](https://getbootstrap.com/) - For front-end styling

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
