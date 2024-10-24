from django.views.generic import TemplateView
from .models import Product, UserFlow



# this is the main index view
class IndexView(TemplateView):
    template_name = 'myPageflows/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nav_items'] = [
            {
                'title': 'FILTERS',
                'url': '#',
                'icon': 'fa-solid fa-list-ul'
            },
            {
                'title': 'ALL',
                'url': '#'
            },
            {
                'title': 'DOWNLOADING YOUR CONTENT',
                'url': '#'
            },
            {
                'title': 'INVITING PEOPLE',
                'url': '#'
            },
            {
                'title': 'ONBOARDING',
                'url': '#'
            },
            {
                'title': 'UPGRADING YOUR ACCOUNT',
                'url': '#'
            },

        ]

        context['products'] = Product.objects.all()

        return context


class ProductView(TemplateView):
    template_name = 'myPageflows/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['product_id']
        context['product'] = Product.objects.get(id=product_id)
        context['user_flow'] = UserFlow.objects.filter(product=context['product'])
        return context