# Authentication System Documentation

## Overview
This Django blog application uses Django's built-in authentication framework to manage user accounts securely. The system supports user registration, login, logout, and profile management. Passwords are stored securely using Django's built-in hashing algorithms, and all forms are protected with CSRF tokens.

---

## Components Breakdown

### 1. User Model
- Uses Django’s built-in `User` model.
- Stores username, email, and hashed password.
- Extended using a `Profile` model to store additional fields such as bio and profile image.

### 2. Registration
- Handled using a custom form extending `UserCreationForm`.
- Validates password strength and confirmation.
- Automatically hashes passwords.
- URL: `/register`

### 3. Login & Logout
- Uses Django’s built-in `LoginView` and `LogoutView`.
- Login authenticates user credentials and starts a session.
- Logout ends the user session.
- URLs:
  - `/login`
  - `/logout` (POST method for security)

### 4. Profile Management
- Restricted to authenticated users using `login_required`.
- Users can update their email, bio, and profile image.
- Signals automatically create a `Profile` for new users.
- URL: `/profile`

### 5. Security Measures
- CSRF tokens on all forms.
- Passwords are hashed automatically.
- Protected routes require login.
- Session-based authentication ensures safe user sessions.

---

## How Users Interact

1. **Register:** Users create an account with username, email, and password.
2. **Login:** Users log in with their credentials to access protected pages.
3. **Profile:** Authenticated users can view and edit their profile details.
4. **Logout:** Users submit the logout form to securely end their session.

---

## Testing the Authentication System

1. Start the server:
```bash
python manage.py runserver
