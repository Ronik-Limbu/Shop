from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.title
    
class SubCategory(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    
    def __str__(self) -> str:
        return self.title + "-----"+ self.category.title
    
class Product(models.Model):
    image=models.ImageField(upload_to='prodcuts',null=True,blank=True)
    image2=models.ImageField(upload_to='prodcuts',null=True,blank=True)
    image3=models.ImageField(upload_to='prodcuts',null=True,blank=True)
    
    name=models.CharField(max_length=50)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    desc=RichTextField(blank=True)
    mark_price=models.DecimalField(max_digits=10,decimal_places=2)
    descount_percent=models.DecimalField(max_digits=4,decimal_places=2)
    price=models.DecimalField(max_digits=10,decimal_places=2,editable=False)
    date=models.DateField(auto_now=True)
    
    def save(self,*args, **kwargs):
        self.price=self.mark_price *(1-self.descount_percent/100)
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.name
    
    
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to="profile_picture",blank=True,null=True)
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.user.username
        
        
class Review(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    rating=models.PositiveIntegerField()
    comment=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.product.name
    
    
    