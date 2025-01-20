from django.db.models.signals import post_migrate
from django.dispatch import receiver

from marketplace.marketplace.settings import roles


@receiver(post_migrate)
def create_or_update_roles(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission  # Импортируем модели внутри функции
    from django.core.exceptions import ObjectDoesNotExist

    for role_key, role_data in roles.items():
        # Создаем или получаем группу
        group, _ = Group.objects.get_or_create(name=role_data['name'])

        # Проверяем и добавляем разрешения
        for perm_codename in role_data['permissions']:
            try:
                permission = Permission.objects.get(codename=perm_codename)
                if permission not in group.permissions.all():
                    group.permissions.add(permission)
            except ObjectDoesNotExist:
                print(f"Permission `{perm_codename}` does not exist. Please check your permissions.")
