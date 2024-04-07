from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        queryset = Product.objects.select_related('collection')
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        return Response({"ping": "pong"})


@api_view()
def product_detail(request, id):
    return Response({"detail ping": "pong"})


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            products_count=Count('products')
        )
        serilaizer = CollectionSerializer(queryset, many=True)
        return Response(serilaizer.data)
    elif request.method == 'POST':
        serilaizer = CollectionSerializer(data=request.data)
        serilaizer.is_valid(raise_exception=True)
        serilaizer.save()
        return Response(serilaizer.data)


@api_view(['DELETE', 'GET'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    collection.products_count = collection.products.count()

    if request.method == 'DELETE':
        if collection.products_count > 0:
            return Response({'message': 'Has products'}, status=status.HTTP_400_BAD_REQUEST)

        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(CollectionSerializer(collection).data)
