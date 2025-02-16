#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # Set the default Django settings module for the 'manage.py' utility.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kairos.settings')

    try:
        # Import the execute_from_command_line function from Django.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Handle ImportError if Django is not installed or not in the Python path.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Execute the command-line arguments using Django's management utility.
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    # Run the main function when the script is executed.
    main()
