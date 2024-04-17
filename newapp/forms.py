from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        widgets = {
            'country': forms.Select(attrs={'class': 'country-select'}),
        }
        phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel'}))
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise forms.ValidationError("Phone number must be 10 digits long.")
        return phone_number
