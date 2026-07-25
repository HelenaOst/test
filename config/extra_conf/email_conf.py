import os

#mailtrap
# SMTP backend для продакшену (розкоментувати і налаштувати)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 2525))
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
MANAGERS_EMAIL = os.environ.get('MANAGERS_EMAIL', 'moderation@automarket.com')

# Console backend для розробки
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#MANAGERS_EMAIL = os.environ.get('MANAGERS_EMAIL', 'moderation@automarket.com')