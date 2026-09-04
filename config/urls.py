from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.html",
        subject_template_name="registration/password_reset_subject.txt",
    ), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
    path("password-change/", auth_views.PasswordChangeView.as_view(
        template_name="registration/password_change_form.html"), name="password_change"),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="registration/password_change_done.html"), name="password_change_done"),

    path("", include("apps.dashboard.urls")),
    path("incidents/", include("apps.incidents.urls")),
    path("risk-assessments/", include("apps.risk.urls")),
    path("job-safety-analyses/", include("apps.risk.jsa_urls")),
    path("toolbox-talks/", include("apps.risk.toolbox_urls")),
    path("inspections/", include("apps.inspections.urls")),
    path("ppe/", include("apps.ppe.urls")),
    path("fire-equipment/", include("apps.fire.urls")),
    path("training/", include("apps.training.urls")),
    path("first-aiders/", include("apps.training.first_aiders_urls")),
    path("osh-committee/", include("apps.training.committee_urls")),
    path("capa/", include("apps.capa.urls")),
    path("doshs-reports/", include("apps.doshs.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("companies/", include("apps.organizations.urls")),
    path("search/", include("apps.core.search_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
