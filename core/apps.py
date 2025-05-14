from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)

def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    group_names = ['Casa Matriz', 'Supervisor', 'Auditor', 'Tienda']
    for name in group_names:
        Group.objects.get_or_create(name=name)