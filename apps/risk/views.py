from apps.core.generic import build_crud_views
from .models import RiskAssessment, JobSafetyAnalysis, ToolboxTalk

ListView, CreateView, UpdateView, DeleteView = build_crud_views(
    model=RiskAssessment,
    fields=['site', 'activity', 'hazards_identified', 'existing_controls', 'likelihood', 'severity', 'status', 'review_date'],
    url_namespace="risk",
    page_title="Risk Assessment",
)

JSAListView, JSACreateView, JSAUpdateView, JSADeleteView = build_crud_views(
    model=JobSafetyAnalysis,
    fields=['task_name', 'steps', 'hazards', 'ppe_required'],
    url_namespace="jsa",
    page_title="Job Safety Analysis",
)

ToolboxListView, ToolboxCreateView, ToolboxUpdateView, ToolboxDeleteView = build_crud_views(
    model=ToolboxTalk,
    fields=['site', 'topic', 'summary', 'attendees_count', 'held_on', 'ai_generated'],
    url_namespace="toolbox",
    page_title="Toolbox Talk",
)
