from django.contrib import admin
from .models import Topping, Pizza

# Register your models here.

admin.site.register(Topping)


@admin.register(Pizza)
class PassengersAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title', )
    }