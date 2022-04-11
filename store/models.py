from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @property
    def total_customers(self):
        return Customer.objects.all().count()


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.CharField(max_length=255, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='images/', default="images/placeholder.png")
    image1 = models.ImageField(upload_to='images/', default="images/placeholder.png")
    image2 = models.ImageField(upload_to='images/', default="images/placeholder.png")
    image3 = models.ImageField(upload_to='images/', default="images/placeholder.png")
    image4 = models.ImageField(upload_to='images/', default="images/placeholder.png")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"

    @property
    def imageURL(self):
        return self.image.url if hasattr(self, 'image') and hasattr(self.image, 'url') else ''

    @property
    def image1URL(self):
        return self.image1.url if hasattr(self, 'image1') and hasattr(self.image1, 'url') else ''

    @property
    def image2URL(self):
        return self.image2.url if hasattr(self, 'image2') and hasattr(self.image2, 'url') else ''

    @property
    def image3URL(self):
        return self.image3.url if hasattr(self, 'image3') and hasattr(self.image3, 'url') else ''

    @property
    def image4URL(self):
        return self.image4.url if hasattr(self, 'image4') and hasattr(self.image4, 'url') else ''

    @property
    def total_products(self):
        return Product.objects.all().count()


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    def __iter__(self):
        return iter(self.orderitem_set.all())

    @property
    def shipping(self):
        return not all(item.product.digital for item in self)

    @property
    # prijs
    def get_cart_total(self):
        return sum([item.get_total for item in self])

    @property
    # hoeveelheid producten
    def get_cart_items(self):
        return sum([item.quantity for item in self])

    @property
    # product naam
    def get_cart_products(self):
        return "\n".join([item.product.name for item in self])

    @property
    def total_orders(self):
        return Order.objects.all().count()

    @property
    def total_omzet(self):
        value = f'{round(sum(item.get_cart_total for item in Order.objects.all()), 2):,}'
        # return value.replace('.', '/').replace(',', '.').replace('/', ',')
        return value.translate({ord("."): ",", ord(","): "."})

    @property
    def bestseller_name(self):
        counters = dict()
        for item in OrderItem.objects.all():
            counters[item.product.name] = (
                counters[item.product.name] + item.quantity
                if item.product.name in counters
                else item.quantity
            )
        return max(counters, key=counters.get)

    @property
    def bestseller_aantal(self):
        return sum(item.quantity for item in OrderItem.objects.filter(product__name=self.bestseller_name).all())

    @property
    def second_bestseller_name(self):
        counters = dict()
        bestseller_name = self.bestseller_name
        for item in OrderItem.objects.all():
            if item.product.name != bestseller_name:
                counters[item.product.name] = (
                    counters[item.product.name] + item.quantity
                    if item.product.name in counters
                    else item.quantity
                )
        return max(counters, key=counters.get)

    @property
    def second_bestseller_aantal(self):
        return sum(item.quantity for item in OrderItem.objects.filter(product__name=self.second_bestseller_name).all())

    @property
    def third_bestseller_name(self):
        counters = dict()
        bestseller_name = self.bestseller_name
        second_bestseller_name = self.second_bestseller_name
        for item in OrderItem.objects.all():
            if item.product.name not in [bestseller_name, second_bestseller_name]:
                counters[item.product.name] = (
                    counters[item.product.name] + item.quantity
                    if item.product.name in counters
                    else item.quantity
                )
        print("Working:", repr(max(counters, key=counters.get)))
        return max(counters, key=counters.get)

    @property
    def third_bestseller_aantal(self):
        print("Working:", repr(
            sum(item.quantity for item in OrderItem.objects.filter(product__name=self.third_bestseller_name).all())))
        return sum(item.quantity for item in OrderItem.objects.filter(product__name=self.third_bestseller_name).all())

    @property
    def get_quantity_for_all_names(self):
        counters = dict()
        for item in OrderItem.objects.all():
            counters[item.product.name] = (
                counters[item.product.name] + item.quantity
                if item.product.name in counters
                else item.quantity
            )
        return counters

    def get_data(self):
        total_ordered = dict()
        for item in OrderItem.objects.all():
            total_ordered[item.product.name] = (
                total_ordered[item.product.name] + item.quantity
                if item.product.name in total_ordered
                else item.quantity
            )
        toplist = {
            name: total_ordered[name]
            for name in sorted(total_ordered, key=total_ordered.get, reverse=True)
        }
        return toplist

    @property
    def get_top_list(self):
        counters = dict()
        for item in OrderItem.objects.all():
            counters[item.product.name] = (
                counters[item.product.name] + item.quantity
                if item.product.name in counters
                else item.quantity
            )
        return max(counters, key=counters.get)

        print("Not working:", repr(list(self.get_data().keys())))
        return list(self.get_data().keys())

    @property
    def get_toplist_aantal(self):
        print("Not working:", list(self.get_data().values()))
        return list(self.get_data().values())


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_name(self):
        return self.order.customer.name

    @property
    def get_dateOrdered(self):
        return self.order.date_ordered

    @property
    def get_complete(self):
        return self.order.complete

    @property
    def get_transactionID(self):
        return self.order.transaction_id

    @property
    def get_orderID(self):
        return self.order.id

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    postcode = models.CharField(max_length=200, null=False)
    stad = models.CharField(max_length=200, null=False)
    nummer = models.CharField(max_length=30, null=False, default="+31 6")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class contact(models.Model):
    name = models.CharField(max_length=200, default=" ")
    email = models.EmailField(max_length=200, default=" ")
    bericht = models.TextField(max_length=200, default=" ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact"
