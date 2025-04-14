from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class UsersConfig(AppConfig):
    # Best Practice: Explicit primary key type
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Best Practice: Use full Python path
    name = 'users'  
    
    # Best Practice: Translation-ready verbose name
    verbose_name = _('User Management')
    
    # Best Practice: Type hints for better IDE support
    def ready(self) -> None:
        """
        App initialization method.
        Best Practice: Keep imports inside ready() to avoid circular imports
        """
        # Best Practice: Lazy import signals
        from django.conf import settings
        if settings.DEBUG:
            self._register_signals()
            
    def _register_signals(self) -> None:
        """Best Practice: Isolate signal registration"""
        try:
            import users.signals  # noqa F401
        except ImportError as e:
            if settings.DEBUG:
                print(f"Signals not found: {e}")  # Best Practice: Debug output
