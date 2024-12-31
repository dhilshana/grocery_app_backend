from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework .generics import GenericAPIView
from . serializers import RegisterSerializer,LoginSerializer,ProductSerializer,ReviewSerializer,CategorySerializer,WishlistSerializer,CartSerializer,OrderSerializer,AddressSerializer
from . models import Registration,Login,Product,Review,Category,Wishlist,Cart,Order,Address,Review_image
from rest_framework.response import Response
from rest_framework import status
import cloudinary
import cloudinary.uploader
import cloudinary.api
# Create your views here.
def index(request):
    return HttpResponse("haiiiii")

# def register_view(request):
#     return HttpResponse('Register')

class Register_View(GenericAPIView):
    def get_serializer_class(self):
        return RegisterSerializer
    
    def post(self,request):
        login_id = ''
        name = request.data.get('name')
        email = request.data.get('email')
        number = request.data.get('number')
        password = request.data.get('password')
        role = 'user'

        if not name or not email or not number or not password or not role:
            return Response({'message':'All fields are requred'},status=status.HTTP_400_BAD_REQUEST,)
        
        if Registration.objects.filter(email = email).exists():
            return Response({'message':'Duplicate emails are not allowed'},status=status.HTTP_400_BAD_REQUEST)
        
        elif Registration.objects.filter(number = number).exists():
            return Response({'message':'Number already found'},status=status.HTTP_400_BAD_REQUEST)
        

        login_serializer = LoginSerializer(data = {'email':email,'password':password,'role':role})

        if login_serializer.is_valid():
            l = login_serializer.save()
            login_id = l.id

        else :
            return Response({'message':'Login failed','errors':login_serializer.errors},status=status.HTTP_400_BAD_REQUEST,)
        

        register_serializer = RegisterSerializer(
            data = {
                'name' : name,
                'email':email,
                'password':password,
                'number':number,
                'role':role,
                'login_id':login_id

            })
        
        if register_serializer.is_valid():
            register_serializer.save()
            return Response({'message':'Registeration successful','data':register_serializer.data},status=status.HTTP_200_OK,)
        else:
            return Response({'message':'Registration Failed','errors':register_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

class Login_View(GenericAPIView):
    def get_serializer_class(self):
        return LoginSerializer
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Check if both email and password are provided
        if not email or not password:
            return Response({'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists with the given email and password
        loginDetails = Login.objects.filter(email=email, password=password)
        
        if loginDetails.exists():
            storeData = LoginSerializer(loginDetails, many=True)
            
            for i in storeData.data:
                login_id = i['id']
                role = i['role']
            
            # Fetch the name from the Registration table using the login_id
            registerDetails = Registration.objects.filter(login_id=login_id).values()
            if registerDetails.exists():
                name = registerDetails[0]['name']
                return Response(
                    {'data': {'login_id': login_id, 'name': name, 'email': email}, 'message': 'Login successful'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'message': 'User registration details not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Return "User not found" message
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class User_View(GenericAPIView):
    def get_serializer_class(self):
        return RegisterSerializer
    
    def get (self,request):
        users = Registration.objects.all()
        if users.count() > 0:
            register_serializer =RegisterSerializer(users,many = True)
            

            return Response({'data':register_serializer.data,'count':users.count()},status=status.HTTP_200_OK)
            
        else:
            return Response({'message':'No data yet'},status=status.HTTP_400_BAD_REQUEST)
        
class User_View_By_Id(GenericAPIView):
    def get_serializer_class(self):
        return RegisterSerializer
    
    def get(self,request,id):
        user = Registration.objects.get(pk = id)
        serialized_data = RegisterSerializer(user)
        return Response({'data':serialized_data.data})
    
class Delete_Single_User(GenericAPIView):
    def get_serializer_class(self):
        return RegisterSerializer

    def delete(self, request, id):
        try:
            # Get the user from the Registration table
            user = Registration.objects.get(pk=id)
            # Get the associated login entry
            login_entry = user.login_id  # Assuming a ForeignKey relationship exists
            # Delete the user entry
            user.delete()
            # Delete the corresponding login entry
            login_entry.delete()
            return Response({'message': 'Deleted successfully'}, status=status.HTTP_200_OK)
        except Registration.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class Update_Single_User(GenericAPIView):
    def get_serializer_class(self):
        return RegisterSerializer
    
    def put(self,request,id):
        user = Registration.objects.get(pk = id)
        serialized_data = RegisterSerializer(instance=user,data=request.data,partial=True)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'data':serialized_data.data,'message':'Updated successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'message':'Unable to update'},status=status.HTTP_400_BAD_REQUEST)  
cloudinary.config(cloud_name = 'dmyj4sdjd',api_key = '361428599544124',api_secret = 'wfvowr6fhlKkYmdxIrtpYhS0A6U')
class Add_Product(GenericAPIView):
    def get_serializer_class(self):
        return ProductSerializer

    def post(self,request):
        name = request.data.get('name')
        price = request.data.get('price')
        category = request.data.get('category')
        image = request.FILES.get('image')
        unit = request.data.get('unit')
        quantity = request.data.get('quantity')
        desc = request.data.get('desc')
        if not image:
            return Response({'Message':'Please uplaod a valid image'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            upload_data = cloudinary.uploader.upload(image)
            product_data = {
                'name':name,
                'price':price,
                'category':category,
                'image':upload_data['url'],
                'quantity':quantity,
                'unit':unit,
                'desc':desc,
            }
            serialized_data = ProductSerializer(data = product_data)
            if serialized_data.is_valid():
                serialized_data.save()
            
                return Response({'data':serialized_data.data,'message':'Uploaded successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'error':serialized_data.errors},status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)

        

        

       

class View_Product(GenericAPIView):
    def get_serializer_class(self):
        return ProductSerializer
    
    def get(self,request):
        products = Product.objects.all()
        if products.count() > 0:
            serialized_data = ProductSerializer(products,many = True)
            return Response({'data':serialized_data.data},status=status.HTTP_200_OK)
        else:
            return Response({'message':'No data available'},status=status.HTTP_400_BAD_REQUEST)
        

class View_Product_By_Id(GenericAPIView):
    def get_serializer_class(self):
        return ProductSerializer
    
    def get(self,request,id):
        product = Product.objects.get(pk = id)
        serialized_data = ProductSerializer(product)
        return Response({'data':serialized_data.data},status=status.HTTP_200_OK)
    
class Update_Product_By_Id(GenericAPIView):
    def get_serializer_class(self):
        return ProductSerializer
    
    def put(self,request,id):
        product = Product.objects.get(pk = id)
        image = request.FILES.get('image')
        if image:
            try:
                # Upload the new image to Cloudinary
                upload_data = cloudinary.uploader.upload(image)
                request.data['image'] = upload_data['url']
            except Exception as e:
                return Response({'message': f'Image upload failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        serialized_data = ProductSerializer(instance = product, data = request.data,partial = True)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'data':serialized_data.data,'message':'Updated successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'message':'Failed to update'},status=status.HTTP_400_BAD_REQUEST)
        
class Delete_By_Id(GenericAPIView):
    def get_serializer_class(self):
        return ProductSerializer
    
    def delete(self,request,id):
        product = Product.objects.get(pk = id)
        product.delete()
        return Response({'message':'Deleted successfully'},status=status.HTTP_200_OK)
    



class Add_Review(GenericAPIView):
    def get_serializer_class(self):
        return ReviewSerializer

    def post(self, request):
        # Extract data from the request
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')
        description = request.data.get('description')
        rating = request.data.get('rating')
        images = request.FILES.getlist('image')
        print(images)

        # Check for missing image
        if not images:
            return Response({'message': 'Image is required'}, status=status.HTTP_400_BAD_REQUEST)

     
        # Validate rating
        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                return Response({'message': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({'message': 'Invalid rating value. Must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

       
        # Validate product existence
        try:
            product = Product.objects.get(pk=product_id)
            product_name = product.name
        except Product.DoesNotExist:
            return Response({'message': 'No such product'}, status=status.HTTP_404_NOT_FOUND)

        # Validate user existence
        try:
            user = Registration.objects.get(pk=user_id)
            username = user.name
        except Registration.DoesNotExist:
            return Response({'message': 'No such user'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare review data
        review_data = {
            'product_id': product_id,
            'user_id': user_id,
            'product_name': product_name,
            'user_name': username,
            'description': description,
            'rating': rating,
            # 'image': upload_data['url'],
        }

        # Serialize and save review
        serialized_data = ReviewSerializer(data=review_data)
        if serialized_data.is_valid():
            saved_review =  serialized_data.save()
            try:
                for image in images:
                     # Upload image to Cloudinary
                    try:
                        upload_data = cloudinary.uploader.upload(image)
                    except Exception as e:
                        return Response({'message': f'Image upload failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    Review_image.objects.create(image = upload_data['url'],review = saved_review)
            except:
                ''
            return Response({'data': serialized_data.data, 'message': 'Uploaded successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Upload failed", "errors": serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)
  
class View_Review(GenericAPIView):
    def get_serializer_class(self):
        return ReviewSerializer
    
    def get(self,request):
        reviews = Review.objects.all()
        if reviews.count() > 0:
            serialized_data = ReviewSerializer(reviews,many = True)
            return Response({'data':serialized_data.data,'count':reviews.count(),},status=status.HTTP_200_OK)
        else :
            return Response({'message':'No Reviews Yet'},status=status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .models import Review
from .serializers import ReviewSerializer

class View_Review_By_Product_Id(GenericAPIView):
    def get_serializer_class(self):
        return ReviewSerializer

    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)

        if reviews.count() > 0:
            # Serialize the reviews
            serialized_data = ReviewSerializer(reviews, many=True)

            # Extract images for each review
            images = []
            for review_data in serialized_data.data:
                if 'images' in review_data:  # Check if 'images' field exists
                    images.extend(review_data['images'])  # Assuming images is a list for each review

            # Ensure images are unique
            unique_images = list(set(images))

            # Prepare the response
            return Response({
                'data': serialized_data.data,
                'count': reviews.count(),
                'images': unique_images,
            }, status=status.HTTP_200_OK)

        else:
            # If no reviews found
            return Response({'message': 'No Reviews Yet'}, status=status.HTTP_400_BAD_REQUEST)
      
# class Update_Review_By_Id(GenericAPIView):
#     def get_serializer_class(self):
#         return ReviewSerializer
    
#     def put(self,request,id):
#         try:
#             reviewtoupdate = Review.objects.get(pk = id)
#             image = request.FILES.get('image')
#             if image:
#                 try:
#                     # Upload the new image to Cloudinary
#                     upload_data = cloudinary.uploader.upload(image)
#                     request.data['image'] = upload_data['url']
#                 except Exception as e:
#                     return Response({'message': f'Image upload failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#             serialized_data = ReviewSerializer(instance = reviewtoupdate, data = request.data, partial = True)
#             if serialized_data.is_valid():
#                 serialized_data.save()
#                 return Response({'message':'Updated successfully','data':serialized_data.data},status=status.HTTP_200_OK)
#             else:
#                 return Response({'message':'Updation failed'},status=status.HTTP_400_BAD_REQUEST)
            
#         except Review.DoesNotExist:
            # return Response({'message':'Id does not exists'})
        
# class Delete_Review_By_Id(GenericAPIView):
#     def get_serializer_class(self):
#         return ReviewSerializer
    
#     def delete(self,request,id):
#         try:
#             reviewtodelete = Review.objects.get(pk = id)
#             reviewtodelete.delete()
#             return Response({"message":"Deleted successfully"},status=status.HTTP_200_OK)
#         except Review.DoesNotExist:
#             return Response({'message':'Id does not exists'},status=status.HTTP_404_NOT_FOUND)
       
class View_Review_By_Id(GenericAPIView):
    def get_serializer_class(self):
        return ReviewSerializer
    
    def get(self,requst,id):
        try:
            reviewtoview = Review.objects.get(pk = id)
            serialized_data = ReviewSerializer(reviewtoview)
            return Response({'data':serialized_data.data},status=status.HTTP_200_OK)
            
        except Review.DoesNotExist:
            return Response({'message':'Id does not exists'},status=status.HTTP_404_NOT_FOUND)
        
class Add_Categories(GenericAPIView):
    def get_serializer_class(self):
        return CategorySerializer
    def post(self,request):
        category_name = request.data.get('category_name')
        category_image = request.FILES.get('category_image')
        if not category_image:
            return Response({'Message':'Please uplaod a valid image'},status=status.HTTP_400_BAD_REQUEST)
        try:
            upload_data = cloudinary.uploader.upload(category_image)
            category = {
                'category_name':category_name,
                'category_image':upload_data['url'],
            }
            serialized_data = CategorySerializer(data = category,)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message':'Category added successfully'},status=status.HTTP_200_OK)
            else :
                return Response({'message ':'Unable to add category','error':serialized_data.error_messages},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)

        

        
class View_Category(GenericAPIView):
    def get_serializer_class(self):
        return CategorySerializer
    
    def get(self,request):
        category = Category.objects.all()
        if category.count()>0:
            serialized_data = CategorySerializer(category,many = True)
            return Response({'data':serialized_data.data},status=status.HTTP_200_OK)
        else:
            return Response({'message':'No data available'},status=status.HTTP_400_BAD_REQUEST)

class Update_Category(GenericAPIView):
    def get_serializer_class(self):
        return CategorySerializer

    def put(self,request,id):
        try:
            category = Category.objects.get(pk = id)
            image = request.FILES.get('image')
            if image:
                try:
                    # Upload the new image to Cloudinary
                    upload_data = cloudinary.uploader.upload(image)
                    request.data['image'] = upload_data['url']
                except Exception as e:
                    return Response({'message': f'Image upload failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

            serialized_data = CategorySerializer(instance = category,data = request.data,partial = True)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message':'Updated successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'message':'Updation failed'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message':'No such id'},status=status.HTTP_404_NOT_FOUND)
        
class Delete_Category(GenericAPIView):
    def get_serializer_class(self):
        return CategorySerializer
    def delete(self,request,id):
        try:

            categorytodelete = Category.objects.get(pk = id)
            categorytodelete.delete()
            return Response({'message':'Deleted successfully'},status=status.HTTP_200_OK)
        
        except:
            return Response({'message':'No such id'})
        
class View_Products_By_CategoryId(GenericAPIView):
    def get_serializer_class(self):
        return ProductSerializer
    
    def get(self,request,category_id):
        try:
            category = Category.objects.get(pk = category_id)
            products = Product.objects.filter(category_id = category_id)
            serialized_data = ProductSerializer(products,many = True)
            if serialized_data.data:
                return Response({'data ':serialized_data.data},status=status.HTTP_200_OK)
            else:
                return Response({'message':'No data available'},status=status.HTTP_400_BAD_REQUEST)
            
        except Category.DoesNotExist:
            return Response({'message':'Category not found'},status=status.HTTP_404_NOT_FOUND)
        
        
    # def get(self, request, category_id):
    #     if not Category.objects.filter(id=category_id).exists():
    #         return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    #     products = Product.objects.filter(category_id=category_id)
    #     serialized_data = ProductSerializer(products, many=True)
    #     if serialized_data.data:
    #         return Response({'data': serialized_data.data}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'message': 'No products available in this category'}, status=status.HTTP_200_OK)


class Add_Wishlist(GenericAPIView):
    def get_serializer_class(self):
        return WishlistSerializer
    
    def post(self,request):
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')
        if Wishlist.objects.filter(product_id = product_id,user_id = user_id).exists():
            wishlisttodelete = Wishlist.objects.filter(product_id = product_id,user_id = user_id)
            wishlisttodelete.delete()
            return Response({'message':'Removed successfully','status':False},status=status.HTTP_200_OK)
        else:
            product = Product.objects.get(id = product_id)
            product_name = product.name
            product_price = product.price
            product_image = product.image

            producttosave = {
                'product_id' :product_id,
                'user_id':user_id,
                'product_name':product_name,
                'product_price':product_price,
                'product_image':product_image
            }

            serialized_data = WishlistSerializer(data = producttosave)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message':'Added to wishlist successfully','status':True},status=status.HTTP_200_OK)
            else:
                return Response({'message':'Unable to add','error':serialized_data.error_messages},status=status.HTTP_400_BAD_REQUEST)

class Check_Wishlist_Status(GenericAPIView):
    def get_serializer_class(self):
        return WishlistSerializer
    def get(self, request,product_id,user_id):
        is_in_wishlist = Wishlist.objects.filter(product_id=product_id, user_id=user_id).exists()
        return Response({'status': is_in_wishlist}, status=status.HTTP_200_OK)

class View_Wishlist(GenericAPIView):
    def get_serializer_class(self):
        return WishlistSerializer
    def get(self,request,id):
        wishlist = Wishlist.objects.filter(user_id = id)
        if wishlist.count()>0:
            serialzed_data = WishlistSerializer(wishlist,many = True)
            return Response({'data':serialzed_data.data},status=status.HTTP_200_OK)
        else:
            return Response({'message':'No data available'},status=status.HTTP_400_BAD_REQUEST)
        
class Add_Cart(GenericAPIView):
    def get_serializer_class(self):
        return CartSerializer
    def post(self,request):
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')
        if Cart.objects.filter(product_id = product_id,user_id = user_id).exists():
            return Response({'message':'Product already exists'},status=status.HTTP_400_BAD_REQUEST)
        else:
            product = Product.objects.get(id = product_id)
            product_name = product.name
            product_price = product.price
            product_image = product.image
            quantity = product.quantity
            unit = product.unit
            cart_data = {
                'product_id':product_id,
                'user_id':user_id,
                'product_name':product_name,
                'product_price':product_price,
                'product_image':product_image,
                'quantity':quantity,
                'unit':unit
            }
            serialized_data = CartSerializer(data = cart_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message':'Cart added successfully','error':serialized_data.error_messages},status=status.HTTP_200_OK)
            else :
                return Response({'message':'failed to add cart','error':serialized_data.error_messages},status=status.HTTP_400_BAD_REQUEST)
            
class View_Cart(GenericAPIView):
    def get_serializer_class(self):
        return CartSerializer
    
    def get(self,request):
        cart_data = Cart.objects.all()
        
        if cart_data.count() > 0:

            serialized_data = CartSerializer(cart_data,many = True)
            return Response({'data':serialized_data.data},status=status.HTTP_200_OK)
        else:
            return Response({'message':'No data available'})

class View_Cart_By_UserId(GenericAPIView):
    def get_serializer_class(self):
        return CartSerializer

    def get(self,request,id):
        if not Cart.objects.filter(user_id = id):
            return Response({'message':'No carts are added'})
        else:
            cart = Cart.objects.filter(user_id = id)
            total_price = 0
            for item in cart:
                price = float(item.product_price)
                quantity = item.quantity
                total_price = total_price +( price * quantity)
                serialized_data = CartSerializer(cart,many = True)
            if serialized_data.data:
                return Response({'data':serialized_data.data,'Total Price':total_price},status=status.HTTP_200_OK)
            


class Add_Order(GenericAPIView):
    def get_serializer_class(self):
        return OrderSerializer
    
    def post(self,request,id):
        cart_items = Cart.objects.filter(user_id = id,cart_status = 1)

        if cart_items.exists():
            items = []

            for item in cart_items:
                order_items = {
                    'product_id':item.product_id,
                    'product_name':item.product_name,
                    'product_price':item.product_price,
                    'product_image':item.product_image,
                    'user_id':item.user_id,
                    'quantity':item.quantity,
                    'unit':item.unit,
                }
                serialized_data = OrderSerializer(data = order_items)
                if serialized_data.is_valid():
                    serialized_data.save()
            
                    items.append(serialized_data.data)
            cart_items.delete()

            return Response({'message':'Orders placed successfully','data':items},status=status.HTTP_200_OK)
        
        else:
            return Response({'message':'No items in the cart'},status=status.HTTP_400_BAD_REQUEST)
        
class View_Order(GenericAPIView):
    def get_serializer_class(self):
        return OrderSerializer
    
    def get(self,request,id):
        orders = Order.objects.filter(user_id = id)
        if orders.count() > 0:
            serialized_data = OrderSerializer(orders,many = True)
            return Response({'data':serialized_data.data},status=status.HTTP_200_OK)
        else:
            return Response({'message':'No orders yet'},status=status.HTTP_400_BAD_REQUEST)
        
class Add_Address(GenericAPIView):
    def get_serializer_class(self):
        return AddressSerializer
    
    def post(self,request):
        user_id = request.data.get('user_id')
        name = request.data.get('name')
        phone_no = request.data.get('phone_no')
        street_address1 = request.data.get('address1')
        street_address2 = request.data.get('address2')
        city = request.data.get('city')
        state = request.data.get('state')
        country = request.data.get('country')

        address = {
            'user_id':user_id,
            'contact_name':name,
            'phone_number':phone_no,
            'street_address1':street_address1,
            'street_address2':street_address2,
            'city':city,
            'state':state,
            'country':country
        }

        serialized_data = AddressSerializer(data = address)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'message':'Address Saved Successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'message':'Unable to save address','errors': serialized_data.errors},status=status.HTTP_400_BAD_REQUEST)
        
class View_Address(GenericAPIView):
    def get_serializer_class(self):
        return AddressSerializer
    
    def get(self,request):
        addresses = Address.objects.all()
        if addresses.count() > 0:
            serialized_data = AddressSerializer(addresses,many = True)
            return Response({'data':serialized_data.data},status=status.HTTP_200_OK)
        else:
            return Response({'message':'No data yet'},status=status.HTTP_400_BAD_REQUEST)
        
class View_Address_By_UserId(GenericAPIView):
    def get_serializer_class(self):
        return AddressSerializer
    
    def get(self,request,id):
        try:
            address = Address.objects.filter(user_id = id)
            serialized_data = AddressSerializer(address,many=True)
            return Response({'data':serialized_data.data},status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({'message':'No address available'},status=status.HTTP_400_BAD_REQUEST)
        
class Update_Address(GenericAPIView):
    def get_serializer_class(self):
        return AddressSerializer
    
    def put(self,request,id,address_id):
        addressToUpdate = Address.objects.get(user_id = id,id = address_id)
        serialized_data = AddressSerializer(instance = addressToUpdate, data = request.data, partial = True)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'Message':'Address updated successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'Message':'Unable to update address'},status=status.HTTP_400_BAD_REQUEST)
        
class Delete_Address(GenericAPIView):
    def get_serializer_class(self):
        return AddressSerializer
    
    def delete(self,request,id):
        addressToDelete = Address.objects.filter(user_id = id)
        addressToDelete.delete()
        return Response({'Message':'deleted Successfully'},status=status.HTTP_200_OK)


class Delete_Single_Address(GenericAPIView):
    def get_serializer_class(self):
        return AddressSerializer
    
    def delete(self,request,user_id,address_id):
        addressToDelete = Address.objects.get(user_id = user_id,id = address_id)
        addressToDelete.delete()
        return Response({'Message':'deleted Successfully'},status=status.HTTP_200_OK)

        
class SearchProduct(GenericAPIView):
    def get_serializer_class(self):
        return ProductSerializer
    
    def post(self,request):
        search_query = request.data.get('search_query','')
        if search_query:
            products = Product.objects.filter(
                Q(name__icontains = search_query) | Q(category__category_name__icontains = search_query)
                    #icontains is used to search for each element(letter) in the query.
                    # __ is used to join the query with the field,
                    # ie, here the 'name' field in the product table is searched or the category_name in the category table which is joined using the foriegn key as category id is searched
                    #  Q is used to set multiple complex condition in filter() method
            )
            # print('filtered products ',products)
            if not products:
                return Response({'message':'No products found'},status=status.HTTP_400_BAD_REQUEST)
            
            serialized_data = ProductSerializer(products,many = True)
            for product in serialized_data.data:
                if product['image']:
                # Check if the image URL is already absolute
                    if not product['image'].startswith(('http://', 'https://')):
                        product['image'] = settings.MEDIA_URL + product['image']
                    #settings is used to get the original path of the image
                    #ie, here when we fetch the product image('images/image.png') it only takes the image.png
                    # so we use settings to get 'images/image.png'
            return Response({'data':serialized_data.data,'message':'image fetched successfully'},status=status.HTTP_200_OK)
        return Response({'message':'No Query found'},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        search_query = request.query_params.get('search_query','')
        if search_query:
            suggestions = Product.objects.filter(
                Q(name__icontains = search_query) | Q(category__category_name__icontains = search_query)
            ).values('name','category__category_name').distinct()[:10]

            if not suggestions:
                return Response({'Message':'No suggestion found'},status=status.HTTP_404_NOT_FOUND)
            
            suggestion_list = [{'product_name': suggestion['name'], 'category_name': suggestion['category__category_name']} for suggestion in suggestions]
            return Response({'suggestion':suggestion_list,'Message':'Suggestion fetched successfully'},status=status.HTTP_200_OK)
        return Response({'Message':'No query found'},status=status.HTTP_400_BAD_REQUEST)
    
class Change_Password(GenericAPIView):
    def get_serializer_class(self):
        return RegisterSerializer
    
    def put(self,request,id):
        user = get_object_or_404(Registration,pk = id)
        login = user.login_id
        passwordToUpdate = request.data.get('newpassword')
        if passwordToUpdate:
            user.password = passwordToUpdate
            user.save()
            login.password = passwordToUpdate
            login.save()
            serialized_data = RegisterSerializer(user)
            return Response({'data':serialized_data.data,'Success':True,'Message':'Password updated successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'Message':'Please enter the new password'},status=status.HTTP_400_BAD_REQUEST)

        
class Delete_Order(GenericAPIView):
    def get_serializer_class(self):
        return OrderSerializer
    
    def delete(self,request,user_id,order_id):
        orderToDelete = Order.objects.filter(user_id = user_id,id = order_id)
        orderToDelete.delete()
        return Response({'Message':'Order deleted successfully'},status=status.HTTP_200_OK)
    
class Increment_Cart(GenericAPIView):
    def get_serializer_class(self):
        return CartSerializer
    
    def put(self,request,user_id,cart_id):
        cartToIncrement = Cart.objects.get(user_id = user_id,id = cart_id)
        cartToIncrement.quantity +=1
        cartToIncrement.save()
        serialized_data = CartSerializer(cartToIncrement)
        return Response({'Message':'Incremented successfully','data':serialized_data.data},status=status.HTTP_200_OK)


class Decrement_Cart(GenericAPIView):
    def get_serializer_class(self):
        return CartSerializer
    
    def put(self,request,user_id,cart_id):
        cartToIncrement = Cart.objects.get(user_id = user_id,id = cart_id)
        cartToIncrement.quantity -=1
        cartToIncrement.save()
        serialized_data = CartSerializer(cartToIncrement)
        return Response({'Message':'Decremented successfully','data':serialized_data.data},status=status.HTTP_200_OK)
    
class Delete_Cart(GenericAPIView):
    def get_serializer_class(self):
        return CartSerializer
    
    def delete(self,request,user_id,cart_id):
        cartToDelete = Cart.objects.get(user_id = user_id,id = cart_id)
        cartToDelete.delete()
        return Response({'Message':'Item deleted from cart'},status=status.HTTP_200_OK)
    
class Forgot_Password(GenericAPIView):
    def get_serializer_class(self):
        return RegisterSerializer
    
    def post(self,request):
        email = request.data.get('email')
        number = request.data.get('number')
        user = Registration.objects.filter(email = email,number = number).first()
        if not user:
            return Response({'Message':'User does not exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            serialized_data = RegisterSerializer(user)
            user_id = serialized_data.data['id']
            return Response({'id':user_id},status=status.HTTP_200_OK)


    


        




