from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index),
    path('register/',views.Register_View.as_view()),
    path('login/',views.Login_View.as_view()),
    path('users/',views.User_View.as_view()),
    path('user/<int:id>',views.User_View_By_Id.as_view()),
    path('delete/<int:id>',views.Delete_Single_User.as_view()),
    path('update/<int:id>',views.Update_Single_User.as_view()),
    path('addproduct/',views.Add_Product.as_view()),
    path('viewproducts/',views.View_Product.as_view()),
    path('viewsingleproduct/<int:id>',views.View_Product_By_Id.as_view()),
    path('updateproduct/<int:id>',views.Update_Product_By_Id.as_view()),
    path('deleteproduct/<int:id>',views.Delete_By_Id.as_view()),
    path('reviewproduct',views.Add_Review.as_view()),
    path('viewreviews',views.View_Review.as_view()),
    # path('updatereview/<int:id>',views.Update_Review_By_Id.as_view()),
    # path('deletereview/<int:id>',views.Delete_Review_By_Id.as_view()),
    path('viewreviewbyproductid/<int:product_id>',views.View_Review_By_Product_Id.as_view()),
    path('viewreviewbyid/<int:id>',views.View_Review_By_Id.as_view()),
    path('addcategory',views.Add_Categories.as_view()),
    path('viewcategory',views.View_Category.as_view()),
    path('updatecategory/<int:id>',views.Update_Category.as_view()),
    path('deletecategory/<int:id>',views.Delete_Category.as_view()),
    path('viewproductsbycategoryid/<int:category_id>',views.View_Products_By_CategoryId.as_view()),
    path('wishlist',views.Add_Wishlist.as_view()),
    path('checkwishliststatus/<int:product_id>/<int:user_id>',views.Check_Wishlist_Status.as_view()),
    path('viewwishlist/<int:id>',views.View_Wishlist.as_view()),
    path('addcart',views.Add_Cart.as_view()),
    path('viewcart',views.View_Cart.as_view()),
    path('viewcartbyuserid/<int:id>',views.View_Cart_By_UserId.as_view()),
    path('addorder/<int:id>',views.Add_Order.as_view()),
    path('vieworders/<int:id>',views.View_Order.as_view()),
    path('saveaddress',views.Add_Address.as_view()),
    path('viewaddress',views.View_Address.as_view()),
    path('viewaddressbyuserid/<int:id>',views.View_Address_By_UserId.as_view()),
    path('searchproduct',views.SearchProduct.as_view()),
    path('changepassword/<int:id>',views.Change_Password.as_view()),
    path('deleteorder/<int:user_id>/<int:order_id>',views.Delete_Order.as_view()),
    path('incrementcart/<int:user_id>/<int:cart_id>',views.Increment_Cart.as_view()),
    path('decrementcart/<int:user_id>/<int:cart_id>',views.Decrement_Cart.as_view()),
    path('deletecartitem/<int:user_id>/<int:cart_id>',views.Delete_Cart.as_view()),
    path('updateaddress/<int:id>/<int:address_id>',views.Update_Address.as_view()),
    path('deleteaddress/<int:id>',views.Delete_Address.as_view()),
    path('deletesingleaddress/<int:user_id>/<int:address_id>',views.Delete_Single_Address.as_view()),
    path('forgotpassword/',views.Forgot_Password.as_view()),

]
