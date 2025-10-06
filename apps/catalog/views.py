from rest_framework import generics, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.views.generic import TemplateView
from django.core.paginator import Paginator


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.select_related("category").order_by("-created_at")
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


class ProductListPage(TemplateView):
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = self.request.Get.get("q", "").strip()
        qs = Product.objects.select_related("category").order_by("-created_at")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontaions=q))

        paginator = Paginator(qs, 12)
        page_number = self.request.GET.get("page") or 1
        page_obj = paginator.get_page(page_number)

        ctx["q"] = q
        ctx["page_obj"] = page_obj
        ctx["products"] = page_obj.object_list

        return ctx
