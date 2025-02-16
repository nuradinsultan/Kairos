from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

# Swagger/OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Kairos API",
        default_version='v1',
        description="API documentation for Kairos, a Robinhood-like trading platform.",
        terms_of_service="https://kairos.com/terms/",
        contact=openapi.Contact(email="support@kairos.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # API Documentation (Swagger/OpenAPI)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API endpoints
    path('api/auth/', include('users.urls')),  # Authentication endpoints (login, register, etc.)
    path('api/stocks/', include('stocks.urls')),  # Stock trading endpoints
    path('api/transactions/', include('transactions.urls'),  # Transaction history endpoints
    path('api/notifications/', include('notifications.urls')),  # Notification endpoints
    path('api/analytics/', include('analytics.urls')),  # Analytics endpoints
    path('api/social-trading/', include('social_trading.urls')),  # Social trading endpoints
    path('api/gamification/', include('gamification.urls')),  # Gamification endpoints

    # WebSocket endpoints (if needed)
    path('ws/', include('stocks.routing')),  # WebSocket routes for real-time stock updates
    path('ws/', include('notifications.routing')),  # WebSocket routes for real-time notifications
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
