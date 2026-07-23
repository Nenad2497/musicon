from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BandProfile, SendMessageToBand, AddGigDate
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import BandProfileForm, SendMessageToBandForm, AddGigDateForm


def indexView(request):
    featuredBands = BandProfile.objects.order_by('-created_at')[:3]
    today = timezone.now().date()
    upcoming_gigs = AddGigDate.objects.filter(date__gte=today).select_related('user__bandprofile').order_by('date', 'time')
    context = {
        'featuredBands': featuredBands,
        'upcoming_gigs': upcoming_gigs,
    }
    return render(request, 'core/index.html', context)

def checkBandDetails(request,pk):
    band = get_object_or_404(BandProfile, pk=pk)
    form = SendMessageToBandForm()

    if request.method == 'POST':
        form = SendMessageToBandForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.band_profile = band
            message.save()
            messages.success(request, f'Poruka je uspešno poslata bendu {band.name}!')
            return redirect('check_band_details', pk=band.pk)
    genres_list = [genre.strip() for genre in band.genres.split(',') if genre.strip()]

    context = {'band': band, 'genres_list': genres_list, 'form': form}

    return render(request, 'core/band_details.html', context)

def all_bands_view(request):
    band_list = BandProfile.objects.order_by('-created_at')
    paginator = Paginator(band_list, 9) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'core/all_bands.html', context)

def all_gigs_view(request):
    today = timezone.now().date()
    gig_list = AddGigDate.objects.filter(date__gte=today).select_related('user__bandprofile').order_by('date', 'time')
    paginator = Paginator(gig_list, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'core/all_gigs.html', context)

@login_required
def check_new_messages(request):
    unread_count = 0
    try:
        if request.user.bandprofile:
            unread_count = SendMessageToBand.objects.filter(
                band_profile=request.user.bandprofile, 
                is_read=False
            ).count()
    except BandProfile.DoesNotExist:
        pass
    return JsonResponse({'unread_count': unread_count})

@login_required
def mark_messages_as_read(request):
    if request.method == 'POST':
        try:
            if request.user.bandprofile:
                SendMessageToBand.objects.filter(band_profile=request.user.bandprofile, is_read=False).update(is_read=True)
                return JsonResponse({'status': 'success'})
        except BandProfile.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_message(request, message_id):
    if request.method == 'POST':
        try:
            message = get_object_or_404(SendMessageToBand, pk=message_id, band_profile=request.user.bandprofile)
            message.delete()
            return JsonResponse({'status': 'success'})
        except (BandProfile.DoesNotExist, SendMessageToBand.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Not authorized or message not found'}, status=403)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def toggle_message_read_status(request, message_id):
    if request.method == 'POST':
        try:
            message = get_object_or_404(SendMessageToBand, pk=message_id, band_profile=request.user.bandprofile)
            message.is_read = not message.is_read
            message.save()
            return JsonResponse({'status': 'success', 'is_read': message.is_read})
        except (BandProfile.DoesNotExist, SendMessageToBand.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Not authorized or message not found'}, status=403)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def delete_gig(request, gig_id):
    if request.method == 'POST':
        try:
            gig = get_object_or_404(AddGigDate, pk=gig_id, user=request.user)
            gig.delete()
            return JsonResponse({'status': 'success'})
        except AddGigDate.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Not authorized or gig not found'}, status=403)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def AddGigDateView(request):
    if request.method == 'POST':
        form = AddGigDateForm(request.POST)
        if form.is_valid():
            gig = form.save(commit=False)
            gig.user = request.user  
            gig.save()
            messages.success(request, 'Svirka je uspešno dodata!')
        else:
            messages.error(request, 'Greška prilikom dodavanja svirke. Proverite unete podatke.')
    return redirect('index') 

@login_required
def dashboardView(request):
    try:
        profile = request.user.bandprofile
    except BandProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        profile_form = BandProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            new_profile = profile_form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            messages.success(request, 'Profil je uspešno sačuvan!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Došlo je do greške. Molimo proverite formu profila.')
    else:
        profile_form = BandProfileForm(instance=profile)

    context = {
        'profile_form': profile_form,
        'profile': profile
    }
    return render(request, 'core/dashboard.html', context)