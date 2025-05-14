from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

# Decorador genérico para requerir un grupo específico
def group_required(group_name):
    def in_group(user):
        if user.is_superuser or user.groups.filter(name=group_name).exists():
            return True
        raise PermissionDenied
    return user_passes_test(in_group)