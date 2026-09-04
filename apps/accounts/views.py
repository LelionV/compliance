from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .models import User


class OrgAdminRequiredMixin(LoginRequiredMixin):
    """Only an org_admin (client-side HSE officer) may manage their own team.
    Platform admins are deliberately excluded here — they manage users via
    /admin/ across all companies instead."""

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or user.role != User.Role.ORG_ADMIN or user.organization is None:
            raise PermissionDenied("Only an organization admin can manage team members.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(organization=self.request.user.organization)


class TeamMemberForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep unchanged when editing.")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "job_title", "role", "is_active"]
        widgets = {
            "role": forms.Select(choices=[
                (User.Role.ORG_ADMIN, "Organization Admin"),
                (User.Role.ORG_STAFF, "Organization Staff"),
            ])
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        pw = self.cleaned_data.get("password")
        if pw:
            user.set_password(pw)
        elif not user.pk:
            user.set_unusable_password()
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get("class", "")
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = (existing + " form-check-input").strip()
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs["class"] = (existing + " form-select").strip()
            else:
                widget.attrs["class"] = (existing + " form-control").strip()


class TeamListView(OrgAdminRequiredMixin, ListView):
    model = User
    template_name = "accounts/team_list.html"
    context_object_name = "members"


class TeamCreateView(OrgAdminRequiredMixin, CreateView):
    model = User
    form_class = TeamMemberForm
    template_name = "accounts/team_form.html"
    success_url = reverse_lazy("accounts:team_list")

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        messages.success(self.request, "Team member added.")
        return super().form_valid(form)


class TeamUpdateView(OrgAdminRequiredMixin, UpdateView):
    model = User
    form_class = TeamMemberForm
    template_name = "accounts/team_form.html"
    success_url = reverse_lazy("accounts:team_list")

    def form_valid(self, form):
        messages.success(self.request, "Team member updated.")
        return super().form_valid(form)
