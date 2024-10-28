from django.views.generic import TemplateView
from .models import Product, UserFlow
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
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

        context['nav_items'] = [
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

        selected_name = self.request.GET.get('selected_name', None)

        if selected_name is None:
            selected_name = 'iOS User Flows'

        context['selected_name'] = selected_name

        if selected_name and selected_name != 'iOS User Flows':
            context['products'] = Product.objects.filter(title=selected_name)
        else:
            context['products'] = Product.objects.all()

        context['user_flows_with_names_counts'] = (
            Product.objects.annotate(userflow_count=Count('user_flows'))
            .values('title', 'userflow_count')
        )
        return context


class ProductView(TemplateView):
    template_name = 'myPageflows/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['product_id']
        context['product'] = Product.objects.get(id=product_id)
        context['user_flow'] = UserFlow.objects.filter(product=context['product'])
        context['user_flows'] = UserFlow.objects.all()
        print(context['product'])
        print(context['user_flow'])

        return context
