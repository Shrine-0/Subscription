from django.urls import path
from . import views

urlpatterns = [
    path("webhook/",views.stripe_webhook,name="webhook"),
    path("get-all/",views.get_order,name = "get-all"),
    path("add-new/",views.add_order,name = "add-new"),
    path("<int:pk>/update/",views.process_order,name ="update"),
    path("<int:pk>/delete/",views.delete_order,name="delete"),
    path("create-checkout-session/",views.create_checkout_session,name= "create-checkout-session"),
]
