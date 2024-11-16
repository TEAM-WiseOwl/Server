from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include('accounts.urls', namespace='accounts')),
    #path("api/notices/", include('notices.urls', namespace='notices')),
    #path("api/requirements/", include('requirements.urls', namespace='requirements')),
    #path("api/products/", include('products.urls', namespace='products')),
    #path("api/payments/", include('payments.urls', namespace='payments')),
    path("api/", include('facilities.urls',namespace='facilities'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
