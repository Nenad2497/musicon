from django.urls import path
from . import views 


urlpatterns = [
    path('', views.indexView, name='index'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('check-and-details/<int:pk>/', views.checkBandDetails, name='check_band_details'),
    path('bands/', views.all_bands_view, name='all_bands'),
    path('gigs/', views.all_gigs_view, name='all_gigs'),
    path('add-gig-date/', views.AddGigDateView, name='add_gig_date'),
    path('api/check-new-messages/', views.check_new_messages, name='check_new_messages'),
    path('api/mark-messages-as-read/', views.mark_messages_as_read, name='mark_messages_as_read'),
    path('api/messages/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('api/messages/<int:message_id>/toggle-read/', views.toggle_message_read_status, name='toggle_message_read_status'),
    path('api/gigs/<int:gig_id>/delete/', views.delete_gig, name='delete_gig'),
]