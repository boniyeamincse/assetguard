from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Notification

@login_required
def notification_list(request):
    """List all notifications for current user (excluding deleted)"""
    notifications = Notification.objects.filter(recipient=request.user, is_deleted=False)
    unread_count = notifications.filter(is_read=False).count()

    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/list.html', context)

@login_required
def mark_notification_read(request, pk):
    """Mark single notification as read"""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_as_read()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})

    return redirect('notifications:notification_list')

@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(recipient=request.user, is_read=False, is_deleted=False).update(is_read=True)

    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})

    return redirect('notifications:notification_list')

@login_required
def delete_notification(request, pk):
    """Soft delete notification"""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.soft_delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})

    return redirect('notifications:notification_list')

