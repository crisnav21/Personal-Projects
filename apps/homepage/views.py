from django.views.generic import TemplateView
from apps.catalog.models import Product


class HomePage(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured_products"] = Product.objects.select_related("category").order_by(
            "-created_at"
        )[:8]
        return ctx
