from django.db import models
# from django.utils import timezone
# Create your models here.

class User(models.Model):
    email = models.EmailField()
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    mobile = models.PositiveBigIntegerField()
    password = models.CharField(max_length=10)
    picture = models.ImageField(default="",upload_to="profile/")
    role = models.CharField(default="bayer",max_length = 50, null =True)

    def __str__(self):
        return self.firstname

class Product(models.Model):
    category = (
        ("Men","Men"),
        ("Women","Women"), 
        ("Child","Child")
    )
    size = (
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL"),
        ("XLL","XLL"),
        ("XLLL","XLLL")
    )
    brand = (
        ("Levis","Levis"),
        ("Roadstar","Roadstar"),
        ("Trands","Trands"),
        ("Zudio","Zudio"),
        ("Raymond","Raymond")
    )
    pcategory = models.CharField(max_length=20,choices=category,null=True)
    psize = models.CharField(max_length=20,choices=size,null=True)
    pbrand = models.CharField(max_length=20,choices=brand,null=True)
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    desc= models.TextField()
    ppicture=models.ImageField(default="",upload_to="ppicture/")
    pname = models.CharField(max_length=20)
    
    def __str__(self):
        return self.pcategory
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    # date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.user) + " " + str(self.product)
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    # date = models.DateTimeField(default=timezone.now())
    cprice = models.PositiveIntegerField()
    tprice = models.PositiveIntegerField()
    cqty = models.PositiveIntegerField(default = 0)
    payment = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user) + " " + str(self.product)
    
class Ajax(models.Model):
    email = models.EmailField()
    fname = models.CharField(max_length=30)
    mobile = models.PositiveBigIntegerField()

    def __str__(self):
        return self.fname