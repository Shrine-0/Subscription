import os
from django.views import View
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from order.models import Order
from order.serializers import OrderSerializers
from rest_framework.response import Response
from rest_framework import status
from product.models import Product
import stripe
from subscription.settings import STRIPE_PRIVATE_KEY, STRIPE_WEBHOOK_SECERET
from utils.helpers import get_current_host
from django.contrib.auth.models import User
@api_view(["GET"])
def get_order(request):
    order = Order.objects.all()
    # order = get_object_or_404(Order)
    serializer = OrderSerializers(order,many=True)
    return Response({"Order":serializer.data})

@api_view(["POST"])
# @permission_classes([IsAuthenticated,IsAdminUser])
def add_order(request):
    
    # user = request.user #! -- User authentication- ------------- --------------->
    data = request.data
    
    orders = data['order']
    
    if orders and len(orders) == 0:
        return Response({"Error":"No order was made please check and try again"},status = status.HTTP_400_BAD_REQUEST)
    
    else:
        #! -- create order
        for i in orders:
            products = Product.objects.get(id = i['product'])
            order = Order.objects.create(
                product = products,
                # name = products.name,
                user = products.user,
                
                # user=user #! --  user authentication------------>
                
                total_amount = i['total_amount'],
            )
        serailizer = OrderSerializers(order,many= False)
        return Response(serailizer.data)
    
@api_view(["PUT"])
# @permission_classes([IsAdminUser])
def process_order(request,pk):
    # order = Order.objects.get(id = pk)
    order = get_object_or_404(Order,id = pk)
    order.payment_status = request.data["payment_status"]
    order.save()
    serializer = OrderSerializers(order,many=False)
    return Response({"order":serializer.data})

@api_view(["DELETE"])
# @permission_classes([IsAdminUser])
def delete_order(request,pk):
    # order = Order.objects.get(id = pk)
    order = get_object_or_404(Order,id = pk)
    order.delete()
    return Response({"order-details":f"order for id :{pk} is deleted"})


stripe.api_key = STRIPE_PRIVATE_KEY
@api_view(["POST"])
@permission_classes([IsAdminUser]) #! --- authentiaction
def create_checkout_session(request):
    YOUR_DOMAIN = get_current_host(request)

    user = request.user #! --- authentication
    data = request.data
    
    orders = data["order"]
    
    user_details ={
        "user":user.id
    }
    checkout_order_items=[]
    for i in orders:
        checkout_order_items.append({
            "price_data":{
                "currency" : "npr",
                "product_data" : {
                    "name":i["name"],
                    # "images": 
                    "metadata":{"product_id":i["product"]}
                },
                "recurring":{
                    "interval":"year"
                },
                "unit_amount":i["price"]*100
            },
            "quantity":i["quantity"]
        })
    checkout_session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        metadata = user_details,
        line_items = checkout_order_items,
        customer_email = user.email,
        mode = 'subscription',
        subscription_data = {'trial_period_days':7,},
        success_url = YOUR_DOMAIN,
        cancel_url = YOUR_DOMAIN,
        # idempotency_key="keeee"
    )
    return Response({"session":checkout_session})

@api_view(["POST"])
def stripe_webhook(request):
    
    webhook_secret = "whsec_599dbf3f66bece9e8b11c8c2c8bc3927fa67d82a15bf76a8fc1b85b70652aff0"
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload,sig_header,webhook_secret
        )
        
    except ValueError as e:
        return Response({"error":"Invalid Payload - ValueError"},status = status.HTTP_400_BAD_REQUEST)
    
    except stripe.error.SignatureVerificationError as e:
        return Response({"error":"Invalid Signature - SignatureVerificationError"},status = status.HTTP_400_BAD_REQUEST)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        line_items = stripe.checkout.Session.list_line_items(session['id'])
        
        price = session['amount_total']
        
        
        for item in line_items['data']:
            print(f'item : {item}')
            line_product =stripe.Product.retrieve(item.price.product)
            product_id = line_product.metadata.product_id
            product = Product.objects.get(id = product_id)
            item = Order.objects.create(  
            user = User(session.metadata.user),
            total_amount = price,
            payment_mode = "Card",
            payment_status = "Paid",
            product = product,
            )

        return Response({'details':'Payment successful'})
    else:
        return Response({"error": f"Unhandled event type: {event['type']}"}, status=status.HTTP_400_BAD_REQUEST)

