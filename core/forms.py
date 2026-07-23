from django import forms
from .models import BandProfile,AddGigDate,SendMessageToBand


class AddGigDateForm(forms.ModelForm):
    class Meta:
        model = AddGigDate
        exclude = ['user']

class SendMessageToBandForm(forms.ModelForm):
    class Meta:
        model = SendMessageToBand
        fields = [
            "sender_name",
            "sender_email",
            "phone_contact",
            "message",
        ]
class BandProfileForm(forms.ModelForm):
    class Meta:
        model = BandProfile
        exclude = ['user', 'created_at', 'updated_at']