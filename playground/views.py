from django.shortcuts import render
from django.shortcuts import render

from django.db.models import Q, F, Func, Value, ExpressionWrapper, DecimalField
from django.db.models.functions import Pi
from django.db.models.aggregates import Min, Sum, Count

from store.models import Product, OrderItem, Order, Customer
from tag.models import TaggedItem


def say_hello(request):
    name = 'Mahdi'

    # result = Product.objects.filter(
    #     # id__in=OrderItem.objects.values('product_id').distinct() # having relation
    #     # orderitem__id__gt=100 # querying relation
    # ).count()

    # result = Product.objects.select_related('collection')[0:5] # 1-N => we want 1

    # result = Product.objects \
    #     .prefetch_related('orderitem_set')[0:5]  # M-N => we want M
    # result = Order.objects.prefetch_related('orderitem_set__product').get(pk=1)  # we want relation of relation :)

    # result = Product.objects.aggregate(Min('unit_price'), Sum('unit_price'))

    # result = Product.objects.annotate(
    #     orders_count=Count('orderitem')
    # ).filter(orders_count__gt=5).values('title', 'orders_count').order_by('-orders_count')[0:5]

    # result = Product.objects.annotate(
    #     pi=Pi()
    # ).values('pi').first()

    # result = Customer.objects.annotate(
    #     orders_count=Count('order') # relation name should be `order_set`
    # ).values('first_name', 'orders_count').order_by('-orders_count')[0:5]

    # result = Product.objects.annotate(
    #     final_price=ExpressionWrapper(
    #         F('unit_price') * Value(0.8), output_field=DecimalField())
    # ).order_by('-unit_price').values('title', 'final_price')[0:5]

    result = TaggedItem.objects.get_tags_for(Product, 1)
    # result = Product.objects.prefetch_related('tags').filter(id__in=[1, 2])

    return render(
        request,
        'hello.html',
        {
            'name': name,
            'result': result
        }
    )
