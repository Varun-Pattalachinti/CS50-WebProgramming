from django.db import models
from django import forms
# Create your models here.

class Menu(models.Model):
    price = models.DecimalField(max_digits = 5, decimal_places =2)

    def __str__(self):
        return f"{self.id} costs {self.price}"

class Pizza(models.Model):
    PIZZA_TYPE = (
        ('R','Regular Pizza'),
        ('S','Sicilian Pizza')
    )
    NUM_OF_TOPPINGS = (
        (0, 'Cheese'),
        (1, '1 Topping'),
        (2, '2 Topping'),
        (3, '3 Toppings'),
        (4, '4 Toppings/ Special')
    )
    #Like the idea of keeping the size as a
    SIZE = (
        (0,'Small'),
        (1, 'Large')
    )
    pizza_type = models.CharField(choices = PIZZA_TYPE, max_length=1)
    number_of_toppings = models.IntegerField(choices = NUM_OF_TOPPINGS)
    size = models.IntegerField(choices = SIZE)
    menu_listing_price = models.ForeignKey(Menu,on_delete=models.CASCADE,related_name="item_price")

    def __str__(self):
        return f"This pizza is a {self.pizza_type}, has {self.number_of_toppings} and is {self.size} and is {self.menu_listing_price.price}"

class Toppings(models.Model):
    topping = models.CharField(max_length = 64)

    def __str__(self):
        return f"This is {self.topping}"

class Subs(models.Model):

     SIZE = (
         (0,'Small'),
         (1, 'Large')
     )
     NUM_OF_TOPPINGS =(
        (0, 'No toppings'),
        (1, '1 topping'),
        (2, '2 toppings'),
        (3, '3 toppings'),
        (4, '4 toppings')
     )
     type = models.CharField(max_length=64)
     size = models.IntegerField(choices = SIZE)
     num_of_toppings = models.IntegerField(choices = NUM_OF_TOPPINGS)
     menu_listing_price = models.ForeignKey(Menu,on_delete=models.CASCADE,related_name="sub_item_price")

     def sub_price(self):
         return {self.menu_listing_price} + 0.5*{self.num_of_toppings}

     def __str__(self):
         return f"This is a {self.size} {self.type} and costs {self.menu_listing_price.price} "

class sub_toppings(models.Model):
    sub_topping = models.CharField(max_length=64)

    def __str__(self):
        return f"This is {self.sub_topping}"
