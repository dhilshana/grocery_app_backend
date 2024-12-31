from rest_framework import serializers

from . models import Registration,Login,Product,Review,Category,Wishlist,Cart,Order,Address,Review_image

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['user_id', 'product_id', 'product_name', 'user_name', 'time', 'description', 'rating','images']
    def get_images(self,obj):
        review_images =   Review_image.objects.filter(review = obj)
        image_list=[]
        for img in review_images:
            image_list.append(img.image)
        return image_list

class WishlistSerializer(serializers.ModelSerializer):
    class Meta :
        model = Wishlist
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta :
        model = Address
        fields = '__all__'