# Phone Number Constants
ETHIOPIAN_COUNTRY_CODE = '+251'
PHONE_NUMBER_LENGTH = 9  # Without country code
MAX_PHONE_VERIFICATION_ATTEMPTS = 3

# Security Constants
PIN_LENGTH = 6
OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5
MAX_PIN_ATTEMPTS = 3

# Document Constants
ALLOWED_DOCUMENT_TYPES = [
    'national_id',
    'passport',
    'drivers_license',
    'business_license'
]
MAX_DOCUMENT_SIZE_MB = 5

# Onboarding Constants
ONBOARDING_TIMEOUT_DAYS = 7
REQUIRED_AGREEMENTS = [
    'terms_of_service',
    'privacy_policy',
    'electronic_communications'
]

# Demo Account Constants
INITIAL_DEMO_BALANCE = 100000.00  # ETB
MAX_DEMO_RESETS = 3
