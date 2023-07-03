from django.db import models
import inspect
from django.contrib.auth.models import User

class Category(models.TextChoices):
    free = "FREE"
    Premium = "Premium"
    
class Product(models.Model):
    name  = models.CharField(max_length=200,blank=False,choices = Category.choices,default=Category.free)
    description  = models.CharField(max_length= 200 ,default="",blank = False)
    # price  = models.IntegerField(default=0)#centslll
    price  = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    user = models.ForeignKey(User,on_delete= models.SET_NULL,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    # def get_display_price(self):
    #     return "{0:.2f}".format(self.price / 100)
    
    # def __repr__(self):
    #     return self.name
    
# print(inspect.getsource(str()))