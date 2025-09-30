from django.urls import path
from apps.catalog.views import CategoryList, ProductList, ProductListPage

urlpatterns = [
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("products/", ProductList.as_view(), name="product-list"),
    path("", ProductListPage.as_view(), name="catalog-page"),
]
