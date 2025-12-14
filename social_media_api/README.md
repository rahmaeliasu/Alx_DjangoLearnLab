# Social Media API

A Django-based REST API for a social media application. This project features custom user modeling, token-based authentication, and profile management using the Django REST Framework (DRF).

## Features

* **Custom User Model:** Extends Django's default user to include social features like bios, profile pictures, and a following system.
* **Token Authentication:** Secure stateless authentication using DRF Authtoken.
* **Profile Management:** Endpoints for users to register, login, and manage their own profiles.

---

## 1. User Model Overview

The system uses a custom `User` model that extends Django's `AbstractUser`.

| Field | Type | Description |
| :--- | :--- | :--- |
| `username` | String | Unique identifier for the user. |
| `email` | String | User's email address. |
| `password` | String | Hashed and salted password. |
| `bio` | Text | (Optional) Short biography of the user. |
| `profile_picture` | Image | (Optional) Profile avatar. |
| `followers` | ManyToMany | A recursive relationship. `symmetrical=False` means User A following User B does not imply User B follows User A. |

---

## 2. Setup Process

### Prerequisites
* Python 3.8+
* pip

### Installation

1.  **Clone the repository** (if applicable) or navigate to the project folder.

2.  **Create and activate a virtual environment:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install django djangorestframework pillow
    ```

4.  **Apply Migrations:**
    This initializes the database and creates the custom user table.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```

---

## 3. Authentication & Usage

All authentication endpoints are located under `/api/accounts/`.

### A. Register a New User
Create a new account. This will return an authentication token immediately.

* **Endpoint:** `POST /api/accounts/register/`
* **Body (JSON):**
    ```json
    {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "securepassword123",
        "bio": "Hello world!"
    }
    ```
* **Response:** Returns `token`, `user_id`, and `email`.

### B. Login
Obtain an authentication token for an existing user.

* **Endpoint:** `POST /api/accounts/login/`
* **Body (JSON):**
    ```json
    {
        "username": "johndoe",
        "password": "securepassword123"
    }
    ```
* **Response:**
    ```json
    {
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
        "user_id": 1,
        "email": "john@example.com"
    }
    ```

### C. Manage Profile (Authenticated Request)
View or update your own profile details. **You must include the token in the header.**

* **Endpoint:** `GET` or `PUT` `/api/accounts/profile/`
* **Header:**
    ```text
    Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    ```
* **Response:** Returns the user's full profile details including follower counts.

---

## 4. Posts & Comments API

The API provides full CRUD capabilities for Posts and Comments.
**Pagination:** Results are paginated (10 items per page).
**Filtering:** Posts can be searched by title or content.

### Post Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/posts/` | List all posts. |
| `GET` | `/api/posts/?search=keyword` | Search posts by title/content. |
| `POST` | `/api/posts/` | Create a new post (Auth required). |
| `GET` | `/api/posts/{id}/` | Retrieve a single post. |
| `PUT` | `/api/posts/{id}/` | Update a post (Author only). |
| `DELETE` | `/api/posts/{id}/` | Delete a post (Author only). |

### Comment Endpoints
* `GET /api/comments/`: List all comments.
* `POST /api/comments/`: Create a comment. Requires `post` ID in body.
* `PUT /api/comments/{id}/`: Update a comment (Author only).
* `DELETE /api/comments/{id}/`: Delete a comment (Author only).

### Example: Create a Post
**POST** `/api/posts/`
**Header:** `Authorization: Token <your_token>`
**Body:**
```json
{
  "title": "My First Post",
  "content": "This is the content of my social media post."
}
