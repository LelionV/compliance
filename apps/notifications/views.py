from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .models import Notification


def _visible_qs(request):
    """Notifications are org-broadcast, so scope strictly to the active org."""
    if request.organization is None:
        return Notification.objects.none()
    return Notification.objects.filter(organization=request.organization)


@login_required
def notification_list(request):
    qs = _visible_qs(request)[:30]
    data = [
        {
            "id": n.pk,
            "message": n.message,
            "level": n.level,
            "link": n.link,
            "is_read": n.is_read,
            "created_at": n.created_at.strftime("%b %d, %H:%M"),
        }
        for n in qs
    ]
    return JsonResponse({"results": data, "unread_count": _visible_qs(request).filter(is_read=False).count()})


@login_required
@require_POST
def mark_read(request, pk):
    notif = _visible_qs(request).filter(pk=pk).first()
    if notif:
        notif.is_read = True
        notif.save(update_fields=["is_read"])
    return redirect(notif.link if notif and notif.link else "dashboard:home")


@login_required
@require_POST
def mark_all_read(request):
    _visible_qs(request).filter(is_read=False).update(is_read=True)
    return JsonResponse({"ok": True})
