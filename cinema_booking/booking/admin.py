from django.contrib import admin
from django.db import IntegrityError
from .models import Movie, Screening, Seat, Voucher, Ticket
import random, string, uuid

# Register your models here.
admin.site.register(Movie)
admin.site.register(Screening)
admin.site.register(Seat)
admin.site.register(Ticket)

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
