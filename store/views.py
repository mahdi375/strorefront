from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
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


class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.annotate(
            products_count=Count('products')
        )
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):
    def get(sefl, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        collection.products_count = collection.products.count()
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'message': 'Has products!'}, status=status.HTTP_400_BAD_REQUEST)

        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
