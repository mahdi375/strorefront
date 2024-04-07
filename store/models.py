from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator

from tag.models import TaggedItem  # FIXME: Dependency


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1,
        choices=MEMBERSHIP_CHOICES,
        default=MEMBERSHIP_BRONZE,
    )


class Address(models.Model):
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)


class Collection(models.Model):
    title = models.CharField(max_length=255, unique=True)
    featured_product = models.ForeignKey(
        to='Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    def __str__(self) -> str:
        return self.description


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()  # unique=True
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(1, message='unit_price must be grater than 1')
        ]
    )
    inventory = models.IntegerField(
        validators=[
            MinValueValidator(0, message='inventory cant be negative'),
        ],
    )
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        to=Collection,
        on_delete=models.CASCADE,
        related_name='products'
    )
    promotions = models.ManyToManyField(to=Promotion, blank=True)
    tags = GenericRelation(TaggedItem)

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    ORDER_STATUS_PENDING = 'P'
    ORDER_STATUS_COMPLETE = 'C'
    ORDER_STATUS_FAILED = 'F'

    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_PENDING, 'Pending'),
        (ORDER_STATUS_COMPLETE, 'Complete'),
        (ORDER_STATUS_FAILED, 'Failed'),
    ]

    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(
        max_length=1,
        choices=ORDER_STATUS_CHOICES,
        default=ORDER_STATUS_PENDING,
    )


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.RESTRICT)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
