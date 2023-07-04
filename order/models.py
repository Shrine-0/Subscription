from django.db import models
from django.contrib.auth.models import User


from product.models import Product

class PaymentStatus(models.TextChoices):
    Paid = "Paid"
    Unpaid ="Unpaid"
    
class PaymentMode(models.TextChoices):
    Card = "Card"
    Fone_pay ="Fone-pay"
    

    
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    payment_status= models.CharField(max_length=20,blank = False,choices=PaymentStatus.choices,default=PaymentStatus.Unpaid)
    payment_mode = models.CharField(max_length=30,choices=PaymentMode.choices,default = PaymentMode.Card)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=500,default="")
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2,blank= False,default=0)
    
    
    def __str__(self):
        return '{:}'.format(self.id)
    
# class OrderItem(models.Model):
#     product  = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
#     order = models.ForeignKey(Order,on_delete = models.CASCADE,null = True)
#     name = 
    