from django.db import models
from django.contrib.auth.models import User

class CarBrand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Booking(models.Model):

    SERVICE_CHOICES = [
        ('Oil Change', 'Oil Change'),
        ('General Service', 'General Service'),
        ('Major Service', 'Major Service'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
    ]

    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('CNG', 'CNG'),
        ('EV', 'EV'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    # car_brand = models.CharField(max_length=100)
    # car_model = models.CharField(max_length=100)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)


    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)

    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    service_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.car_brand} {self.car_model}"


