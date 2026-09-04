from apps.core.generic import build_crud_views
from .models import TrainingRecord, FirstAiderMarshal, OSHCommitteeMember

ListView, CreateView, UpdateView, DeleteView = build_crud_views(
    model=TrainingRecord,
    fields=['employee_name', 'course_title', 'provider', 'completed_on', 'expires_on', 'certificate'],
    url_namespace="training",
    page_title="Training Record",
)

FirstAiderListView, FirstAiderCreateView, FirstAiderUpdateView, FirstAiderDeleteView = build_crud_views(
    model=FirstAiderMarshal,
    fields=['site', 'employee_name', 'role', 'certified_on', 'certificate_expiry', 'contact_phone'],
    url_namespace="first_aiders",
    page_title="First Aider / Marshal",
)

CommitteeListView, CommitteeCreateView, CommitteeUpdateView, CommitteeDeleteView = build_crud_views(
    model=OSHCommitteeMember,
    fields=['employee_name', 'designation', 'represents', 'term_start', 'term_end'],
    url_namespace="committee",
    page_title="OSH Committee Member",
)
