from apps.organizations.models import Organization


def tenant_context(request):
    ctx = {
        "active_organization": getattr(request, "organization", None),
        "is_all_sites": getattr(request, "is_all_sites", False),
    }
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated and getattr(user, "is_platform_admin", False):
        ctx["switchable_organizations"] = Organization.objects.filter(is_active=True).order_by("name")
    return ctx
