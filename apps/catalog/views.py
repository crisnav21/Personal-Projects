from rest_framework import generics, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.views.generic import ListView


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.select_related("category").order_by("-created_at")
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


class ProductListPage(ListView):
    template_name = "list.html"
    context_object_name = "products"
    queryset = Product.objects.select_related("category").order_by("created_at")
