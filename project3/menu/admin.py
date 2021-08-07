from django.contrib import admin

from .models import Menu,Pizza,Toppings,Subs,sub_toppings
# Register your models here.

admin.site.register(Menu)
admin.site.register(Pizza)
admin.site.register(Toppings)
admin.site.register(Subs)
admin.site.register(sub_toppings)
