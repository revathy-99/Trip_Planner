from django.urls import path
from .views import search_destinations,trip_detail,customize_trip,user_customized_trips
from .views import select_trip, add_travelers, confirm_booking
from .views import view_packages,package_detail,book_package,my_bookings
from .views import add_activity, add_itinerary,confirm_booking,trip_booking_success,package_booking_success
from .views import payment_form,process_payment

urlpatterns = [
    path('search/', search_destinations, name='destination_search'),
    path('destination/<int:pk>/', trip_detail, name='trip_detail'),
    path('customize/<int:pk>/', customize_trip, name='customize_trip'),
    path('customized_trips/', user_customized_trips, name='customized_trips'),
    path('booking/select_trip/', select_trip, name='select_trip'),
    path('booking/add_travelers/<int:trip_id>/', add_travelers, name='add_travelers'),
    path('booking/confirm/<int:booking_id>/', confirm_booking, name='confirm_booking'),
    path('booking/success/<int:booking_id>/', trip_booking_success, name='trip_booking_success'),
    path('packages/', view_packages, name='view_packages'),  # View all packages
    path('packages/<int:pk>/', package_detail, name='package_detail'),  # Package details
    # Add URL for booking a package
    path('packages/<int:pk>/book/', book_package, name='book_package'),
    path('package/success/<int:package_id>/', package_booking_success, name='package_booking_success'),
    path('my_bookings/', my_bookings, name='my_bookings'),
    path('trip/<int:trip_id>/add_activity/', add_activity, name='add_activity'),
    path('trip/<int:trip_id>/add_itinerary/', add_itinerary, name='add_itinerary'),
    #payments urls
    path('payment-form/', payment_form, name='payment_form'),
    path('process-payment/',process_payment, name='process_payment'),
   
    
    
]
   


