from django.contrib import admin
from .models import *
# Register your models here.
# class CategoryAdmin(admin.ModelAdmin):
#     list_display=('name','image','description')

# admin.site.register(Category,CategoryAdmin)
class CategoryAdmin( admin.ModelAdmin):
        ...
admin.site.register(Category,CategoryAdmin)

class ProductAdmin( admin.ModelAdmin):
        ...
admin.site.register(Product,ProductAdmin)

class CartAdmin( admin.ModelAdmin):
        ...
admin.site.register(Cart,CartAdmin)

class FavouriteAdmin( admin.ModelAdmin):
        ...
admin.site.register(Favourite,FavouriteAdmin)