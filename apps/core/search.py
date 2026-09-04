from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

from apps.incidents.models import Incident
from apps.risk.models import RiskAssessment, JobSafetyAnalysis, ToolboxTalk
from apps.training.models import TrainingRecord, FirstAiderMarshal
from apps.capa.models import CorrectiveAction
from apps.doshs.models import DOSHSReport, StatutoryDeadline


@login_required
def global_search(request):
    query = request.GET.get("q", "").strip()
    if request.organization is None and not request.is_all_sites:
        return redirect("dashboard:select_org")

    def scoped(qs):
        return qs if request.is_all_sites else qs.filter(organization=request.organization)

    results = {}
    if query:
        results["Incidents"] = [
            (i, "incidents:edit") for i in scoped(Incident.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ))[:10]
        ]
        results["Risk assessments"] = [
            (r, "risk:edit") for r in scoped(RiskAssessment.objects.filter(activity__icontains=query))[:10]
        ]
        results["Job safety analyses"] = [
            (j, "jsa:edit") for j in scoped(JobSafetyAnalysis.objects.filter(task_name__icontains=query))[:10]
        ]
        results["Toolbox talks"] = [
            (t, "toolbox:edit") for t in scoped(ToolboxTalk.objects.filter(topic__icontains=query))[:10]
        ]
        results["Training records"] = [
            (t, "training:edit") for t in scoped(TrainingRecord.objects.filter(
                Q(employee_name__icontains=query) | Q(course_title__icontains=query)
            ))[:10]
        ]
        results["Employees (first aiders / marshals)"] = [
            (f, "first_aiders:edit") for f in scoped(FirstAiderMarshal.objects.filter(employee_name__icontains=query))[:10]
        ]
        results["CAPA items"] = [
            (c, "capa:edit") for c in scoped(CorrectiveAction.objects.filter(title__icontains=query))[:10]
        ]
        results["DOSHS records"] = [
            (d, "doshs:edit") for d in scoped(DOSHSReport.objects.filter(title__icontains=query))[:10]
        ]
        results["Statutory deadlines"] = [
            (d, None) for d in scoped(StatutoryDeadline.objects.filter(title__icontains=query))[:10]
        ]
        # drop empty buckets
        results = {k: v for k, v in results.items() if v}

    return render(request, "core/search_results.html", {"query": query, "results": results})
