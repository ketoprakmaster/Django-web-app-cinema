from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Movie, Screening, Seat, Ticket, Voucher
import random

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in new user
            messages.success(request,"successfully register")
            return redirect('home')  # Redirect to the home page
    else:
        form = UserCreationForm()
    return render(request, 'booking/register.html', {'form': form})

def movies(request,filter=None):
    filter = request.GET.get("keyword")
    if filter:
        movies = Movie.objects.filter(title__contains=filter)
    else:
        movies = Movie.objects.all()
    if not movies:
        messages.info(request,"no movies was found")
    paginator = Paginator(movies, 8)  # Show 5 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'booking/movies.html', {'page_obj': page_obj})

def screenings(request, movie_id):
    screenings = Screening.objects.filter(movie_id=movie_id)
    if not screenings:
        messages.info(request,"no movie screenings available")
    return render(request, 'booking/screenings.html', {'screenings': screenings})

def seats(request, screening_id):
    screening = get_object_or_404(Screening, pk=screening_id)
    seats = screening.seats.all()  
    context = { 'screening': screening, 'seats': seats}
    return render(request, 'booking/seats.html', context)

@login_required
def booking(request, seat_id):
    seat = get_object_or_404(Seat, pk=seat_id)  
    if seat.is_available and request.method == 'POST':
        voucher = request.POST.get('voucher')
        if voucher:
            try:
                valid_voucher = Voucher.objects.get(code=voucher, is_used=False)
                valid_voucher.is_used = True
                valid_voucher.save()
                seat.is_available = False
                seat.save()
                Ticket.objects.create(user=request.user, seat=seat, voucher=valid_voucher)
                messages.success(request, "Booking successful using voucher!")
                return redirect('home')
            except Voucher.DoesNotExist:
                messages.error(request, "Invalid or already used voucher.") 
    return render(request, 'booking/book_ticket.html', {'seat': seat})

@login_required
def user_tickets(request):
    # Get all tickets for the logged-in user
    tickets = Ticket.objects.filter(user=request.user)
    context = {
        'tickets': tickets
    }
    return render(request, 'booking/user_tickets.html', context)

# def login(request):
#     if request.method == "POST":
        