from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Category
from django.shortcuts import get_object_or_404
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin
from orders.forms import CartAddForm


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(request, "home/detail.html", {'product': product, 'form': form})


class BucketHomeView(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'

    def get(self, request):
        all_bucket_objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': all_bucket_objects})


class BucketObjectDeleteView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_bucket_object_task.delay(key)
        messages.info(request, "Your object will deleted soon", "info")
        return redirect("home:bucket")


class BucketObjectDownloadView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_bucket_object_task.delay(key)
        messages.info(request, "Your file will downloaded soon. check out aws folder in root of your project", "info")
        return redirect("home:bucket")
