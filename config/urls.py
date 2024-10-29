from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include('accounts.urls', namespace='accounts')),
    path("api/notices/", include('notices.urls', namespace='notices')),
    path("api/requirements/", include('requirements.urls', namespace='requirements')),
    path("api/products/", include('products.urls', namespace='products')),
    path("api/payments/", include('payments.urls', namespace='payments'))

]
