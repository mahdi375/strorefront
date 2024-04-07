from django.urls import path
from . import views

urlpatterns = [
    path('collections/', views.collection_list),
    path('collections/<int:pk>', views.collection_detail),
    
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
]
