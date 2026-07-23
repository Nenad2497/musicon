from .models import SendMessageToBand, AddGigDate
from django.db.models import Q

def dashboard_data(request):
    if not request.user.is_authenticated:
        return {}
    all_messages = []
    unread_message_count = 0
    try:
        if request.user.bandprofile:
            profile = request.user.bandprofile
            all_messages = SendMessageToBand.objects.filter(band_profile=profile).order_by('-created_at')
    except Exception:
        pass
    gigs_scheduled = AddGigDate.objects.filter(user=request.user).order_by('date')
    return {
        'messages_received': all_messages,
        'gigs_scheduled': gigs_scheduled,
    }