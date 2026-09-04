from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class OrgRequiredMixin(LoginRequiredMixin):
    """
    Ensures a concrete organization is selected (client users always have one;
    platform admins must pick one from the switcher before viewing tenant data).
    Also scopes querysets/forms to that organization automatically.
    """
    model = None
    org_field = "organization"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response

    def get(self, request, *args, **kwargs):
        if request.organization is None and not getattr(request, "is_all_sites", False):
            return redirect("dashboard:select_org")
        if request.organization is None and getattr(request, "is_all_sites", False):
            return redirect("dashboard:select_org")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.organization is None:
            raise PermissionDenied("No organization selected.")
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**{self.org_field: self.request.organization})

    def form_valid(self, form):
        setattr(form.instance, self.org_field, self.request.organization)
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # never let client pick a different organization via a hidden field trick
        if self.org_field in form.fields:
            del form.fields[self.org_field]
        # scope any FK fields that themselves point at org-scoped models
        for name, field in form.fields.items():
            if isinstance(field, forms.ModelChoiceField):
                qs = field.queryset
                if hasattr(qs.model, self.org_field):
                    field.queryset = qs.filter(**{self.org_field: self.request.organization})
            # bootstrap styling
            widget = field.widget
            existing = widget.attrs.get("class", "")
            if isinstance(widget, (forms.CheckboxInput,)):
                widget.attrs["class"] = (existing + " form-check-input").strip()
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs["class"] = (existing + " form-select").strip()
            else:
                widget.attrs["class"] = (existing + " form-control").strip()
        return form


class PlatformAdminRequiredMixin(LoginRequiredMixin):
    """Restricts a view to platform admins (the auditing organization's staff)."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, "is_platform_admin", False):
            raise PermissionDenied("Platform admin access only.")
        return super().dispatch(request, *args, **kwargs)
