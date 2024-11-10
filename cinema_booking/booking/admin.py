from django.contrib import admin
from django.db import IntegrityError
from .models import Movie, Screening, Seat, Voucher, Ticket
import random, string, uuid

# Register your models here.

@admin.action(description='Generate new vouchers')
def generate_vouchers(modeladmin, request, queryset):
    num_vouchers = 10  # Define how many vouchers to create
    created_count = 0
    for _ in range(num_vouchers):
        code = str(uuid.uuid4())  # Generate a new UUID for the voucher
        try: # Try creating the voucher. If it already exists (duplicate UUID), it will raise an IntegrityError.
            Voucher.objects.create(code=code)
            created_count += 1
        except IntegrityError:
            continue
    modeladmin.message_user(request, f'{num_vouchers} vouchers have been successfully generated.')

class TicketsAdmin(admin.ModelAdmin):
    list_display = ["__str__","seat","booking_time",]
    search_fields = ["user","seat"]
admin.site.register(Ticket,TicketsAdmin)

class SeatsAdmin(admin.ModelAdmin):
    list_display = ["__str__","seat_number","screening"]
    search_fields = ["seat_number","screening"]
    list_filter = ["is_available"]
admin.site.register(Seat,SeatsAdmin)

class ScreeningsAdmin(admin.ModelAdmin):
    list_display = ["movie","screening_time","cinema_hall","available_seats"]
    search_fields = ["cinema_hall","movie"]
    list_filter = ["cinema_hall"]
admin.site.register(Screening,ScreeningsAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ["__str__","release_date","duration",]
    search_fields = ["title"]
    list_filter = ["genre"]
admin.site.register(Movie,MovieAdmin)

class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_until', 'is_used')
    search_fields = ['code']
    list_filter = ['is_used']
    actions = [generate_vouchers]
    
    def save_model(self, request, obj, form, change):
        while True:
            obj.code = str(uuid.uuid4())  # Automatically generate a UUID code if none exists
            try:
                obj.save()
                break
            except IntegrityError:
                continue
        super().save_model(request, obj, form, change)
admin.site.register(Voucher, VoucherAdmin)
