from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

STATE_CHOICES = (
    ('Chittagong','Chittagong'),
    ('Dhaka','Dhaka'),
    ('Rajshahi','CRajshahi'),
    ('Khulna','Khulna'),
    ('Shylet','Shylet'),
    ('Borisal','Borisal'),
)

CATEGORY_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

class Product(models.Model):
    title = models.CharField(max_length=100)
    fee = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    school = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    lawyer_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATE_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATE_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class rej(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    number = models.IntegerField(max_length=20)

