from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="Your API Description",
        contact=openapi.Contact(email="your-email@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    path('admin/', admin.site.urls),
    path('auth/', include('user.urls', namespace='user')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('notification.urls'), name='notification'),
    path('', include('product.urls')),
    path('', include('favorite.urls')),
    path('', include('coupon.urls')),
    # User login and token endpoints

    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),

    path("docs/", include_docs_urls(title="PriceWise API", public=False)),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)  # New
