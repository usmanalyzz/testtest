from django.views.generic import TemplateView, ListView
from .models import Product, UserFlow
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages


class RegisterView(View):
    def get(self, request):
        return render(request, 'myPageflows/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'myPageflows/register.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'myPageflows/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return HttpResponseRedirect(reverse_lazy('login'))


class CustomLoginView(LoginView):
    template_name = 'myPageflows/login.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'myPageflows/forget.html'
    email_template_name = 'forget.html'
    success_url = reverse_lazy('login')


class IndexView(TemplateView):
    template_name = 'myPageflows/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.all()

        selected_name = self.request.GET.get('selected_name', None)
        category = self.request.GET.get('category', None)

        if selected_name == 'all_user_flows':
            context['products'] = products
            context['selected_name'] = 'All Products'
        else:
            if category:
                products = products.filter(category=category)
                context['selected_name'] = f"{category} User Flows"
                context['filter_products'] = products.filter(category=category)
            elif selected_name:
                products = products.filter(title=selected_name)
                context['selected_name'] = selected_name
                context['filter_products'] = products.filter(title=selected_name)
            else:
                context['selected_name'] = 'Products'
                context['filter_products'] = products

        context['products'] = products

        context['nav_items'] = [
            {
                'title': product.title,
                'url': f'?selected_name={product.title}'
            }
            for product in products[:5]
        ]

        context['user_flows_with_names_counts'] = (
            Product.objects.annotate(userflow_count=Count('user_flows'))
            .values('title', 'userflow_count')
        )

        context['remaining_products'] = products[5:]

        return context


class Userflows(TemplateView):
    template_name = 'myPageflows/userflow.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all user flows
        user_flows = UserFlow.objects.all()

        selected_name = self.request.GET.get('selected_name', None)
        category = self.request.GET.get('category', None)

        if selected_name == 'all_user_flows':
            context['filter_user_flows'] = user_flows
            context['selected_name'] = 'All User Flows'
        else:
            if category:
                user_flows = user_flows.filter(category=category)
                context['selected_name'] = f"{category} User Flows"
                context['filter_user_flows'] = user_flows.filter(category=category)
            elif selected_name:
                user_flows = user_flows.filter(name=selected_name)
                context['selected_name'] = selected_name
                context['filter_user_flows'] = user_flows.filter(name=selected_name)
            else:
                context['selected_name'] = 'User Flows'
                context['filter_user_flows'] = user_flows

            context['filter_user_flows'] = user_flows

        context['user_flows_with_names_counts'] = (
            UserFlow.objects
            .values('name')
            .annotate(userflow_count=Count('id'))
        )

        context['total_user_flows'] = user_flows.count()

        context['nav_items'] = [
            {
                'name': user_flow.name,
                'url': f'?selected_name={user_flow.name}'
            }
            for user_flow in user_flows.distinct()[:5]
        ]

        context['remaining_user_flows'] = user_flows.distinct()[5:]

        return context


class UserFlowDetail(ListView):
    model = UserFlow
    template_name = 'myPageflows/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_id = self.kwargs.get('product_id')
        context['product_id'] = product_id
        a_product = Product.objects.get(id=product_id)

        product_user_flows = UserFlow.objects.filter(product=a_product).annotate(screenshot_count=Count('screenshots'))

        selected_user_flow = product_user_flows.first() if product_user_flows.exists() else None

        selected_user_flow_screenshot_count = selected_user_flow.screenshots.count() if selected_user_flow else 0

        context['product'] = a_product
        context['user_flows'] = product_user_flows
        context['selected_user_flow'] = selected_user_flow
        context['selected_user_flow_screenshot_count'] = selected_user_flow_screenshot_count
        context['category'] = product_user_flows

        return context


class UserFlowDetailAPI(ListView):
    model = UserFlow
    template_name = 'myPageflows/products.html'

    def get_userflow_product(self, product_id):
        return UserFlow.objects.filter(product_id=product_id).annotate(screenshot_count=Count('screenshots'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_flow_id = self.kwargs['user_flow_id']

        selected_user_flow = UserFlow.objects.get(id=user_flow_id)
        product = selected_user_flow.product
        screenshot_count = selected_user_flow.screenshots.count()

        user_flows = self.get_userflow_product(product.id)

        context['selected_user_flow'] = selected_user_flow
        context['selected_user_flow_screenshot_count'] = screenshot_count
        context['product'] = product
        context['user_flows'] = user_flows
        context['category'] = UserFlow.objects.filter(id=user_flow_id)

        return context
