from django import forms
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import PlatformAdminRequiredMixin
from .models import Organization, Site


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "slug", "dosh_reg_no", "industry", "seats", "logo", "is_active"]
        help_texts = {"slug": "Used in URLs and generated file names. Auto-fills from the name if left blank."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False
        for name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get("class", "")
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = (existing + " form-check-input").strip()
            else:
                widget.attrs["class"] = (existing + " form-control").strip()

    def clean_slug(self):
        from django.utils.text import slugify
        slug = self.cleaned_data.get("slug") or slugify(self.cleaned_data.get("name", ""))
        return slugify(slug)


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["name", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class OrganizationListView(PlatformAdminRequiredMixin, ListView):
    model = Organization
    template_name = "organizations/organization_list.html"
    context_object_name = "organizations"
    queryset = Organization.objects.all().order_by("name")


class OrganizationCreateView(PlatformAdminRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/organization_form.html"
    success_url = reverse_lazy("organizations:list")

    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.name}" added. You can now switch into their portal.')
        return super().form_valid(form)


class OrganizationUpdateView(PlatformAdminRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/organization_form.html"
    success_url = reverse_lazy("organizations:list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["sites"] = self.object.sites.all()
        ctx["site_form"] = SiteForm()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Organization updated.")
        return super().form_valid(form)


class OrganizationDeleteView(PlatformAdminRequiredMixin, DeleteView):
    model = Organization
    template_name = "organizations/organization_confirm_delete.html"
    success_url = reverse_lazy("organizations:list")


class SiteCreateView(PlatformAdminRequiredMixin, CreateView):
    model = Site
    form_class = SiteForm

    def form_valid(self, form):
        form.instance.organization_id = self.kwargs["org_pk"]
        response = super().form_valid(form)
        messages.success(self.request, f'Site "{form.instance.name}" added.')
        return response

    def get_success_url(self):
        return reverse_lazy("organizations:edit", args=[self.kwargs["org_pk"]])


class SiteDeleteView(PlatformAdminRequiredMixin, DeleteView):
    model = Site

    def get_queryset(self):
        return Site.objects.filter(organization_id=self.kwargs["org_pk"])

    def get_success_url(self):
        return reverse_lazy("organizations:edit", args=[self.kwargs["org_pk"]])
