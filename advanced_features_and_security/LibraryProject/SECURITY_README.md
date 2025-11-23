Security measures:

- DEBUG is False in production.
- SESSION_COOKIE_SECURE & CSRF_COOKIE_SECURE set True to ensure cookies sent only over HTTPS.
- X_FRAME_OPTIONS=DENY to prevent clickjacking.
- SECURE_CONTENT_TYPE_NOSNIFF and SECURE_BROWSER_XSS_FILTER enabled.
- Use django-csp for Content Security Policy. Example policy in settings.
- All forms include {% csrf_token %}. AJAX uses X-CSRFToken header.
- Use Django Forms/ORM to avoid SQL injection.
- Sanitize user-supplied HTML using bleach before saving/displaying.
  Testing:
- Manual tests for CSRF, XSS, SQLi, header checks described in the project README.
