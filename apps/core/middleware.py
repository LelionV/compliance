from apps.organizations.models import Organization

SESSION_KEY = "active_organization_id"


class OrganizationMiddleware:
    """
    Resolves request.organization for every request.

    - Platform admins: the "active" organization they've selected via the
      switcher is stored in session. If none selected yet, defaults to the
      first available organization (or None -> "All sites" views).
    - Org (client) users: always locked to their own organization, session
      value is ignored entirely so they can never see another company's data.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.organization = None
        request.is_all_sites = False

        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated:
            if getattr(user, "is_platform_admin", False):
                org_id = request.session.get(SESSION_KEY)
                if org_id == "ALL":
                    request.is_all_sites = True
                    request.organization = None
                elif org_id:
                    request.organization = Organization.objects.filter(pk=org_id, is_active=True).first()
                if request.organization is None and not request.is_all_sites:
                    # default to "All sites" the first time
                    request.is_all_sites = True
            else:
                # Client / org staff — hard-locked, cannot be overridden.
                request.organization = user.organization

        response = self.get_response(request)
        return response
