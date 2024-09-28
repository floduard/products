from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('Kigali City - Gasabo', 'Gasabo'),
    ('Kigali City - Kicukiro', 'Kicukiro'),
    ('Kigali City - Nyarugenge', 'Nyarugenge'),
    ('Northern Province - Burera', 'Burera'),
    ('Northern Province - Gakenke', 'Gakenke'),
    ('Northern Province - Gicumbi', 'Gicumbi'),
    ('Northern Province - Musanze', 'Musanze'),
    ('Northern Province - Rulindo', 'Rulindo'),
    ('Southern Province - Gisagara', 'Gisagara'),
    ('Southern Province - Huye', 'Huye'),
    ('Southern Province - Kamonyi', 'Kamonyi'),
    ('Southern Province - Muhanga', 'Muhanga'),
    ('Southern Province - Nyamagabe', 'Nyamagabe'),
    ('Southern Province - Nyanza', 'Nyanza'),
    ('Southern Province - Nyaruguru', 'Nyaruguru'),
    ('Southern Province - Ruhango', 'Ruhango'),
    ('Eastern Province - Bugesera', 'Bugesera'),
    ('Eastern Province - Gatsibo', 'Gatsibo'),
    ('Eastern Province - Kayonza', 'Kayonza'),
    ('Eastern Province - Kirehe', 'Kirehe'),
    ('Eastern Province - Ngoma', 'Ngoma'),
    ('Eastern Province - Nyagatare', 'Nyagatare'),
    ('Eastern Province - Rwamagana', 'Rwamagana'),
    ('Western Province - Karongi', 'Karongi'),
    ('Western Province - Ngororero', 'Ngororero'),
    ('Western Province - Nyabihu', 'Nyabihu'),
    ('Western Province - Nyamasheke', 'Nyamasheke'),
    ('Western Province - Rubavu', 'Rubavu'),
    ('Western Province - Rusizi', 'Rusizi'),
    ('Western Province - Rutsiro', 'Rutsiro'),
)




CATEGORY_CHOICES = (
    ('G', 'Ghee'),
    ('CB', 'ChickenBatter'),
    ('CW', 'ChickenWings'),
    ('C', 'Chicken'),
    ('M', 'MilkShake'),
    ('F', 'Fish'),
    ('B', 'Beef'),
    ('E', 'Eggs'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')



    def __str__(self):
        return self.title



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField(default=0)
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return self.name