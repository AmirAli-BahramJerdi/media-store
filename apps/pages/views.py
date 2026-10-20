from django.views.generic import TemplateView
from apps.shop.models import Product


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["products"] = Product.objects.filter(is_active=True)
        return ctx