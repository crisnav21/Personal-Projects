from django.contrib import admin
from django.urls import path, include
from apps.cart.views import CartPage

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/v1/catalog/", include("apps.catalog.urls")),
    path("api/v1/cart/", include("apps.cart.urls")),
    path("cart/", CartPage.as_view(), name="cart-page"),
]
