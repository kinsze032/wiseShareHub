from django.contrib import admin

from goodHands.models import Category, Institution, Donation


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')


class DonationAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'institution', 'phone_number', 'city', 'pick_up_date', 'user')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Donation, DonationAdmin)
