from django.urls import path
from .views import CartView, CartAddView, CartLineView, CartPage

urlpatterns = [
    path("", CartView.as_view(), name="cart-detail"),
    path("add/", CartAddView.as_view(), name="cart-add"),
    path("line/<int:line_id>/", CartLineView.as_view(), name="cart-line"),
    path("", CartPage.as_view(), name="cart-page"),
]
