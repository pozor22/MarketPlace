from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

from marketplace.settings import roles


class Command(BaseCommand):
    help = "Create or update predefined user roles with specific permissions"

    def handle(self, *args, **kwargs):
        for role_key, role_data in roles.items():
            group, created = Group.objects.get_or_create(name=role_data['name'])
            if created:
                self.stdout.write(f"Created group: {role_data['name']}")
            else:
                self.stdout.write(f"Group already exists: {role_data['name']}")

            # Добавляем недостающие разрешения
            for perm_codename in role_data['permissions']:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    if not group.permissions.filter(id=permission.id).exists():
                        group.permissions.add(permission)
                        self.stdout.write(f"Added permission `{perm_codename}` to group `{role_data['name']}`")
                except ObjectDoesNotExist:
                    self.stdout.write(f"Permission `{perm_codename}` does not exist. Skipping.")

        self.stdout.write("Roles initialization complete.")
