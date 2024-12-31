from django.contrib import admin

from . models import Registration,Login,Category,Product,Review,Wishlist,Cart,Order,Address,Review_image

# Register your models here.

admin.site.register(Registration)
admin.site.register(Login)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Review_image)