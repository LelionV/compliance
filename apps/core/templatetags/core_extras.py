from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def get_attribute(obj, field_name):
    if obj is None:
        return ""
    value = getattr(obj, field_name, "")
    # resolve choice fields nicely: e.g. status -> get_status_display
    display_method = getattr(obj, f"get_{field_name}_display", None)
    if callable(display_method):
        return display_method()
    if hasattr(value, "all"):  # m2m safety, not used currently
        return ", ".join(str(v) for v in value.all())
    return value


@register.simple_tag
def ns_url(namespace, action, pk=None):
    if pk is not None:
        return reverse(f"{namespace}:{action}", args=[pk])
    return reverse(f"{namespace}:{action}")
