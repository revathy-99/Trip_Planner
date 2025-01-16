from django.shortcuts import render,redirect,get_object_or_404 
from .forms import CustomizationForm,ActivityForm, ItineraryForm
from .models import Destination, Customization,Booking,TripPackage
from .forms import SelectTripForm, TravelerDetailsForm,PackageBookingForm
from django.contrib.auth.decorators import login_required
from .models import Destination, Activity, Itinerary,Booking,Transaction
from django.contrib.auth.models import User
from django.contrib import messages


def search_destinations(request):
    query = request.GET.get('query', '')
    if query:
        destinations = Destination.objects.filter(
            location__icontains=query
        ) | Destination.objects.filter(
            type__icontains=query
        )
    else:
        destinations = Destination.objects.all()

    return render(request, 'Trip_app/search.html', {'destinations': destinations})
@login_required
def trip_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    return render(request, 'Trip_app/trip_detail.html', {'destination': destination})
@login_required
def customize_trip(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == "POST":
        form = CustomizationForm(request.POST)
        if form.is_valid():
            customization = form.save(commit=False)
            customization.user = request.user
            customization.destination = destination
            customization.save()
            form.save_m2m()  # Save many-to-many data
            return redirect('trip_detail', pk=destination.pk)
    else:
        form = CustomizationForm()

    return render(request, 'Trip_app/customize_trip.html', {'form': form, 'destination': destination})
@login_required
def user_customized_trips(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users to login
    
    customized_trips = Customization.objects.filter(user=request.user).select_related('destination')
    return render(request, 'Trip_app/customized_trips.html', {'customized_trips': customized_trips})
@login_required
def select_trip(request):
    """View for selecting a trip."""
    if request.method == 'POST':
        form = SelectTripForm(request.POST)
        if form.is_valid():
            trip = form.cleaned_data['trip']
            return redirect('add_travelers', trip_id=trip.id)
    else:
        form = SelectTripForm()

    return render(request, 'Trip_app/select_trip.html', {'form': form})
@login_required
def add_travelers(request, trip_id):
    """View for adding traveler details."""
    trip = get_object_or_404(Destination, id=trip_id)

    if request.method == 'POST':
        form = TravelerDetailsForm(request.POST)
        if form.is_valid():
            traveler_details = form.save(commit=False)
            traveler_details.user = request.user
            traveler_details.trip = trip
            # Calculate total price
            traveler_details.total_price = trip.price
            traveler_details.save()
            return redirect('confirm_booking', booking_id=traveler_details.id)
    else:
        form = TravelerDetailsForm()

    return render(request, 'Trip_app/add_travelers.html', {'form': form, 'trip': trip})
from django.contrib import messages

@login_required
def confirm_booking(request, booking_id):
    """View for confirming booking."""
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking.status = 'Confirmed'
        booking.save()

        # Add a success message
        messages.success(request, f"Your booking for {booking.trip.name} has been successfully confirmed!")

        return redirect('trip_booking_success', booking_id=booking.id)

    return render(request, 'Trip_app/confirm_booking.html', {'booking': booking})
login_required
def trip_booking_success(request, booking_id):
    """View for trip booking success."""
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'Trip_app/trip_booking_success.html', {'booking': booking})
@login_required
def view_packages(request):
    packages = TripPackage.objects.all()  # Get all the packages from the database
    return render(request, 'Trip_app/view_packages.html', {'packages': packages})
@login_required
def package_detail(request, pk):
    package = get_object_or_404(TripPackage, pk=pk)
    return render(request, 'Trip_app/package_detail.html', {'package': package})

@login_required
@login_required
def book_package(request, pk):
    """View for booking a package."""
    package = get_object_or_404(TripPackage, pk=pk)

    if request.method == 'POST':
        form = PackageBookingForm(request.POST)
        if form.is_valid():
            # Save the booking using the form's save method
            booking = form.save(user=request.user)  # Pass the current user
            # Add a success message
            messages.success(request, f"Your booking for the package {package.name} has been successfully confirmed!")
            return redirect('package_booking_success', package_id=package.pk)
    else:
        form = PackageBookingForm(initial={'package': package})

    return render(request, 'Trip_app/book_package.html', {'form': form, 'package': package})

@login_required
def package_booking_success(request, package_id):
    """View for package booking success."""
    package = get_object_or_404(TripPackage, pk=package_id)
    
    # Assuming you've already created the booking successfully, fetch it here
    booking = Booking.objects.filter(user=request.user, trip=package.destinations.first()).last()
    
    return render(request, 'Trip_app/package_booking_success.html', {'booking': booking})


@login_required
def my_bookings(request):
    """View to display the user's bookings."""
    user_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Trip_app/my_bookings.html', {'bookings': user_bookings})

def add_activity(request, trip_id):
    trip = get_object_or_404(Destination, id=trip_id)
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.destination = trip
            activity.save()
            return redirect('trip_detail', pk=trip_id)
    else:
        form = ActivityForm()
    return render(request, 'Trip_app/add_activity.html', {'form': form, 'trip': trip})

def add_itinerary(request, trip_id):
    trip = get_object_or_404(Destination, id=trip_id)
    if request.method == "POST":
        form = ItineraryForm(request.POST)
        if form.is_valid():
            itinerary = form.save(commit=False)
            itinerary.user = request.user
            itinerary.trip = trip
            itinerary.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('trip_detail', pk=trip_id)
    else:
        form = ItineraryForm()
    return render(request, 'Trip_app/add_itinerary.html', {'form': form, 'trip': trip})

from django.shortcuts import render, get_object_or_404

def payment_form(request):
    booking_id = request.GET.get('booking_id')
    amount = request.GET.get('amount')
    return render(request, 'Trip_app/payment_form.html', {
        'booking_id': booking_id,
        'amount': amount,
    })
from django.http import JsonResponse
import uuid

def process_payment(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        proof = request.FILES.get('proof', None)

        # Simulate a transaction ID
        transaction_id = uuid.uuid4().hex

        # Create a transaction record
        transaction = Transaction.objects.create(
            user=request.user,
            booking_id=booking_id,
            amount=amount,
            payment_method=payment_method,
            proof=proof,
            status="Pending Verification",
            transaction_id=transaction_id
        )

        # Update booking payment status
        booking = get_object_or_404(Booking, id=booking_id)
        booking.payment_status = "Pending Verification"
        booking.save()

        return JsonResponse({"status": "Payment submitted successfully", "transaction_id": transaction_id})
    return JsonResponse({"error": "Invalid request"})

  