from django.urls import path 
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/token/",TokenObtainPairView.as_view(),name = "token_obtain_pair"),
    path("api/token/refersh",TokenRefreshView.as_view(),name = "token_refresh"),
    path("register/",views.register,name ="register"),
    path("me/",views.get_user,name="get-user"),
]
