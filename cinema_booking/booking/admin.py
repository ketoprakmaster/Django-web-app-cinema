from django.contrib import admin
from .models import Movie, Screening, Seat, Voucher, Ticket
import random, string

# Register your models here.
admin.site.register(Movie)
admin.site.register(Screening)
admin.site.register(Seat)
admin.site.register(Ticket)

@admin.action(description='Generate new vouchers')
def generate_vouchers(modeladmin, request, queryset):
    num_vouchers = 10  # Define how many vouchers to create
    for _ in range(num_vouchers):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        Voucher.objects.create(code=code)

    modeladmin.message_user(request, f'{num_vouchers} vouchers have been successfully generated.')

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'user')
    actions = [generate_vouchers]