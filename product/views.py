
from typing import Any
from django.shortcuts import get_object_or_404, render
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import templates
from django.shortcuts import redirect
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status


stripe.api_key  = settings.STRIPE_PRIVATE_KEY 

@api_view(['GET'])
def get_products(request):
    filterset = ProductFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    # product = Product.objects.all()
    serializer = ProductSerializer(filterset.qs,many = True)
    return Response({"Products": serializer.data,})
    
@api_view(['GET'])
def get_product(request,pk):
    # product  = Product.objects.get(id = pk)
    product = get_object_or_404(Product,id = pk) #! ------ adds the object not found logic ----!#
    serializer = ProductSerializer(product,many=False)
    return Response({"id":serializer.data})

@api_view(["POST"])
@permission_classes([IsAuthenticated,IsAdminUser])
def add_product(request):
    user = request.user
    data = request.data
    
    product = data['product']
    
    for i in product:
        product = Product.objects.create(
            name = i['name'],
            description = i['description'],
            price = i['price'],
            user = user,
        )
    serializer = ProductSerializer(product,many=False)
    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_product(request,pk):
    product = get_object_or_404(Product,id = pk)
    if product.user != request.user:
        return Response({"Details":f"Permission-Denied current user {request.user.email} not allowed to perform the actions requested"},status=status.HTTP_401_UNAUTHORIZED)
    product.price = request.data['price']
    product.description = request.data['description']
    product.name = request.data['name']
    product.save()  
    serializer=ProductSerializer(product,many=False)
    return Response({f"updated : {pk}":serializer.data})

@api_view(["DELETE"])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_product(request,pk):
    data =request.data
    user =request.user
    # product = Product.objects.get(id=pk)
    product = get_object_or_404(Product,id=pk)
    if product.user != request.user:
        return Response({"Details":f"Permission-Denied current user {request.user.email} not allowed to perform the actions requested"},status=status.HTTP_401_UNAUTHORIZED)

    product.delete()
    return Response({"product-details":{f"product for id  : {pk} deleted successfully"}})
    
class ProductLandingPageView(TemplateView):
    template_name = "checkout.html"
    
    def get_context_data(self, **kwargs):
        product = Product.objects.get(id = 4)
        context =  super(ProductLandingPageView,self).get_context_data(**kwargs)
        context.update({
            "products":product,
            "STRIPE_PUBLIC_KEY":settings.STRIPE_PUBLIC_KEY,  
        })
        return context

class CreateCheckoutSessionView(View):

    YOUR_DOMAIN = "http://localhost:8000"
        
    # def success(request):
    #     return render(request,"success.html")
    
    # def post(self,request,*args,**kwargs): 
    #     checkout_session = stripe.checkout.Session.create(
    #         line_items=[
    #             {
    #                 # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
    #                 'price': 'price_1NPkztGvjAuWKVBt95bi330D',
    #                 'quantity': 1,
    #             },
    #         ],
            
    #         mode='payment',
    #         # mode='subscription',  # mode is of three types : payment , subscription , and setup #! ----------------------------------------------------------------------
             
    #         success_url=CreateCheckoutSessionView.YOUR_DOMAIN ,
    #         cancel_url=CreateCheckoutSessionView.YOUR_DOMAIN ,
    #     )
    #     # if checkout_session.id :
    #     #     return render(request,"success.html")
    #     # return JsonResponse({
    #     #     "id": checkout_session.id,
    #     #     "session":checkout_session
    #     # },)
    #     # response = redirect(checkout_session.url)
    #     # response.status_code = 303
    #     return redirect(checkout_session.url)
        

