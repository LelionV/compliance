import csv

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .mixins import OrgRequiredMixin


def export_csv(list_view_instance, model, fields):
    """Streams the org-scoped queryset for this list view as a CSV download."""
    queryset = model.objects.filter(organization=list_view_instance.request.organization)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{model._meta.model_name}_export.csv"'
    writer = csv.writer(response)
    writer.writerow(fields)
    for obj in queryset:
        row = []
        for f in fields:
            display_method = getattr(obj, f"get_{f}_display", None)
            value = display_method() if callable(display_method) else getattr(obj, f, "")
            row.append(value)
        writer.writerow(row)
    return response


def build_crud_views(*, model, fields, list_template=None, form_template=None, url_namespace, page_title):
    """
    Returns (ListView, CreateView, UpdateView, DeleteView) classes scoped to the
    active organization, using one generic template set so we don't hand-write
    a template per module.
    """

    class _List(OrgRequiredMixin, ListView):
        pass

    _List.model = model
    _List.template_name = list_template or "core/generic_list.html"
    _List.context_object_name = "objects"
    _List.paginate_by = 25

    def list_get_context_data(self, **kwargs):
        ctx = super(_List, self).get_context_data(**kwargs)
        ctx["page_title"] = page_title
        ctx["fields"] = fields
        ctx["add_url"] = reverse_lazy(f"{url_namespace}:add")
        ctx["url_namespace"] = url_namespace
        return ctx

    _List.get_context_data = list_get_context_data

    def list_get(self, request, *args, **kwargs):
        if request.GET.get("export") == "csv":
            return export_csv(self, model, fields)
        return OrgRequiredMixin.get(self, request, *args, **kwargs)

    _List.get = list_get

    class _Create(OrgRequiredMixin, CreateView):
        pass

    _Create.model = model
    _Create.fields = fields
    _Create.template_name = form_template or "core/generic_form.html"
    _Create.success_url = reverse_lazy(f"{url_namespace}:list")

    def create_get_context_data(self, **kwargs):
        ctx = super(_Create, self).get_context_data(**kwargs)
        ctx["page_title"] = f"Add {page_title}"
        return ctx

    _Create.get_context_data = create_get_context_data

    class _Update(OrgRequiredMixin, UpdateView):
        pass

    _Update.model = model
    _Update.fields = fields
    _Update.template_name = form_template or "core/generic_form.html"
    _Update.success_url = reverse_lazy(f"{url_namespace}:list")

    def update_get_context_data(self, **kwargs):
        ctx = super(_Update, self).get_context_data(**kwargs)
        ctx["page_title"] = f"Edit {page_title}"
        return ctx

    _Update.get_context_data = update_get_context_data

    class _Delete(OrgRequiredMixin, DeleteView):
        pass

    _Delete.model = model
    _Delete.template_name = "core/generic_confirm_delete.html"
    _Delete.success_url = reverse_lazy(f"{url_namespace}:list")

    return _List, _Create, _Update, _Delete
