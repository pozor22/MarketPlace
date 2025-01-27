from django.core.management.base import BaseCommand
from products.models import Category

from marketplace.blanks import categories


class Command(BaseCommand):
    help = "Create or update predefined user roles with specific permissions"

    def handle(self, *args, **kwargs):
        for role_key, role_data in categories.items():
            category, created = Category.objects.get_or_create(
                name=role_data['name'],
                description=role_data['description'])
            if created:
                self.stdout.write(f"Created category: {role_data['name']}")
            else:
                self.stdout.write(f"Group category exists: {role_data['name']}")

        self.stdout.write("Category initialization complete.")
