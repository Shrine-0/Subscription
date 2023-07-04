from django.urls import path
from . import views

from .views import CreateCheckoutSessionView, ProductLandingPageView

urlpatterns = [
    path("create-checkout-session/",CreateCheckoutSessionView.as_view(),name="create-checkout-session"),
    path("", ProductLandingPageView.as_view(), name="Product_page"),
    path("get-all/",views.get_products,name="get-all"),
    path("get-all/<str:pk>/",views.get_product,name="get-all-pk"),
    path("add-product/",views.add_product,name="add-product"),
    path("<int:pk>/update-price/",views.update_price,name="update-price"),
    path("<int:pk>/delete-product/",views.delete_product,name ="delete-product"),
]
