# forms.py in Trip_app
from django import forms
from .models import Customization, Accommodation, Activity,Destination, Booking,TripPackage,Itinerary

class DestinationSearchForm(forms.Form):
    location = forms.CharField(required=False, label="Location")
    date = forms.DateField(required=False, label="Date", widget=forms.DateInput(attrs={'type': 'date'}))
    budget = forms.DecimalField(required=False, label="Budget")
    type = forms.ChoiceField(required=False, label="Type", choices=[('', 'All'), ('Adventure', 'Adventure'), ('Leisure', 'Leisure')])

class CustomizationForm(forms.ModelForm):
    class Meta:
        model = Customization
        fields = ['selected_accommodations', 'selected_activities']

    selected_accommodations = forms.ModelMultipleChoiceField(
        queryset=Accommodation.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    selected_activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class SelectTripForm(forms.Form):
    trip = forms.ModelChoiceField(
        queryset=Destination.objects.all(),
        label="Select a Trip",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class TravelerDetailsForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['traveler_name', 'traveler_email', 'traveler_phone', 'additional_travelers']
        widgets = {
            'traveler_name': forms.TextInput(attrs={'class': 'form-control'}),
            'traveler_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'traveler_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'additional_travelers': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'traveler_name': "Your Name",
            'traveler_email': "Your Email",
            'traveler_phone': "Your Phone Number",
            'additional_travelers': "Additional Travelers (Comma-Separated)",
        }


from django import forms
from .models import Booking, TripPackage

class PackageBookingForm(forms.Form):
    package = forms.ModelChoiceField(queryset=TripPackage.objects.all(), widget=forms.HiddenInput)
    number_of_people = forms.IntegerField(min_value=1)
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())

    def save(self, user):
        # Create a new booking instance (without saving yet)
        package = self.cleaned_data['package']
        number_of_people = self.cleaned_data['number_of_people']
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        # You may want to calculate the total price based on number of people and package price
        total_price = package.price * number_of_people

        # Create the booking object
        booking = Booking.objects.create(
            user=user,
            trip=package.destinations.first(),  # You may want to customize how you link this
            traveler_name=user.username,  # Example: Using the username, or prompt for name
            traveler_email=user.email,  # Assuming the user model has an email
            traveler_phone="",  # Optional: You can ask for phone number if necessary
            additional_travelers="",  # If you plan to allow adding other travelers
            total_price=total_price,
            status='Pending',  # Default status
            created_at=start_date  # You can adjust this field as per your requirement
        )

        return booking


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'price', 'duration']

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['day', 'activities']
        widgets = {
            'activities': forms.CheckboxSelectMultiple(),
        }
