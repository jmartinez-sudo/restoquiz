# core/templatetags/permissions.py
from django import template

register = template.Library()

@register.filter(name="has_group")
def has_group(user, group_name):
    """
    Devuelve True si el usuario pertenece al grupo dado.
    Uso en template:
        {% if request.user|has_group:"Administradores" %}
    """
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()
