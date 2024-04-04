from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(request,fileName):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,fileName)
    return os.path.join('uploads/',new_filename)
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0-show,1-hidden')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=200,null=False,blank=False)
    vendor=models.CharField(max_length=200,null=False,blank=False)
    product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0-show,1-hidden')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name}"
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qnty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name}"

    @property
    def total_cost(self):
        return self.product_qnty*self.product.selling_price

class Favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name}"