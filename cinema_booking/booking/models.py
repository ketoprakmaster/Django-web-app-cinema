import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    genre = models.CharField(max_length=50)
    poster_image = models.ImageField(upload_to='movie_posters/', null=True, blank=True)  

    def __str__(self):
        return self.title

class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="screenings")
    screening_time = models.DateTimeField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.movie.title} at {self.screening_time} in {self.cinema_hall}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the screening is being created for the first time
        super().save(*args, **kwargs)
        # Create seats only if this is a new Screening instance
        if is_new:
            for seat_num in range(1, self.available_seats + 1):
                Seat.objects.create(screening=self, seat_number=seat_num)


class Seat(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=5)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"[{"Available" if self.is_available else "Unavailable"}] seats at {self.seat_number} for {self.screening}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['screening', 'seat_number'], name='unique_seat_per_screening')
        ]

class Voucher(models.Model):
    code = models.CharField(max_length=100, unique=True)
    is_used = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.code

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Ticket for {self.user.username} - Seat {self.seat.seat_number}"


