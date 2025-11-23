# Django Permissions & Groups Setup

This project uses Django's built-in permissions and group system to control
access to `Article` model actions.

## Custom Permissions

Custom permissions are defined inside the Article model’s Meta class:

- can_view: Allows viewing articles
- can_create: Allows creating articles
- can_edit: Allows editing articles
- can_delete: Allows deleting articles

## Groups

Three groups are created and managed via Django admin:

1. Viewers
   - can_view

2. Editors
   - can_view
   - can_create
   - can_edit

3. Admins
   - All permissions (or assign via superuser)

## Permission Checks in Views

Views are protected using `@permission_required`:

```python
@permission_required("bookshelf.can_edit", raise_exception=True)
def article_edit(request, pk):
