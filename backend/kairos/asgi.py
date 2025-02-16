"""
ASGI config for Kairos project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

# Set the default Django settings module for the 'asgi' application.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kairos.settings')

# Get the default Django ASGI application
django_asgi_app = get_asgi_application()

# Import WebSocket routing (if you have WebSocket endpoints)
from stocks.routing import websocket_urlpatterns as stocks_websocket_routes
from notifications.routing import websocket_urlpatterns as notifications_websocket_routes

# Combine WebSocket routes
websocket_routes = (
    stocks_websocket_routes + notifications_websocket_routes
)

# Define the ASGI application
application = ProtocolTypeRouter({
    # HTTP requests are handled by Django's ASGI application
    "http": django_asgi_app,

    # WebSocket requests are handled by the AuthMiddlewareStack and URLRouter
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_routes
        )
    ),
})
