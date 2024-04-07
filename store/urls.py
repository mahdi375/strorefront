from django.urls import path
from . import views

urlpatterns = [
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>', views.CollectionDetail.as_view()),

    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
]
