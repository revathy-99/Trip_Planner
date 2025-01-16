# models.py in Trip_app
from django.db import models
from django.contrib.auth.models import User

class Destination(models.Model):
    name = models.CharField(max_length=100,default='Unknown Destination')
    location = models.CharField(max_length=100,default='Unknown')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50, choices=[('Adventure', 'Adventure'), ('Leisure', 'Leisure')],default='Leisure')
    itinerary = models.TextField(default='Itinerary details go here')
    reviews = models.TextField(default='No reviews yet.')
    available_from = models.DateField(default='2024-01-01')
    available_to = models.DateField(default='2024-12-31')
    image = models.ImageField(upload_to='destination_images/', default='destination_images/default_image.jpg')

    def __str__(self):
        return f"{self.name} - {self.location}"
class Accommodation(models.Model):
    destination = models.ForeignKey(Destination, related_name='accommodations', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()
    available_to = models.DateField()

    def __str__(self):
        return self.name

class Activity(models.Model):
    destination = models.ForeignKey(Destination, related_name='activities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)  # e.g., '2 hours', 'full day'
    
    def __str__(self):
        return self.name

class Customization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    selected_accommodations = models.ManyToManyField(Accommodation, blank=True)
    selected_activities = models.ManyToManyField(Activity, blank=True)

    def __str__(self):
        return f"Customization for {self.user.username} - {self.destination.name}"
    
class TripPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    destinations = models.ManyToManyField(Destination, related_name='packages')  # Linking multiple destinations
    accommodations = models.ManyToManyField(Accommodation, related_name='packages')
    activities = models.ManyToManyField(Activity, related_name='packages')
    meals_included = models.BooleanField(default=True)  # Whether meals are included

    def __str__(self):
        return self.name

class Itinerary(models.Model):
    user = models.ForeignKey(User, related_name='itineraries', on_delete=models.CASCADE)
    trip = models.ForeignKey(Destination, related_name='itineraries', on_delete=models.CASCADE)
    day = models.IntegerField()
    activities = models.ManyToManyField(Activity, related_name='itineraries')

    def __str__(self):
        return f"Day {self.day} - {self.trip.name}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Not Paid', 'Not Paid'),
        ('Pending Verification', 'Pending Verification'),
        ('Paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Destination, on_delete=models.CASCADE)
    package = models.ForeignKey(TripPackage, on_delete=models.CASCADE, null=True, blank=True) 
    traveler_name = models.CharField(max_length=100)
    traveler_email = models.EmailField()
    traveler_phone = models.CharField(max_length=15)
    additional_travelers = models.TextField(blank=True, help_text="List additional traveler names separated by commas")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Not Paid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.trip.name} - {self.status} ({self.payment_status})"
class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    STATUS_CHOICES = [
        ('Pending Verification', 'Pending Verification'),
        ('Verified', 'Verified'),
        ('Failed', 'Failed'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="transactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    proof = models.FileField(upload_to='payment_proofs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Verification')
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} for {self.booking.id} - {self.status}"
