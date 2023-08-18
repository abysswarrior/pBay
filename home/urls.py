from django.urls import path, include
from . import views

app_name = 'home'

bucket_urls = [
    path('', views.BucketHomeView.as_view(), name='bucket'),
    path('object/delete/<path:key>', views.BucketObjectDeleteView.as_view(), name='bucket_object_delete'),
    path('object/download/<path:key>', views.BucketObjectDownloadView.as_view(), name='bucket_object_download'),
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('categories/<slug:category_slug>', views.HomeView.as_view(), name="category"),
    path('bucket/', include(bucket_urls)),
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
]