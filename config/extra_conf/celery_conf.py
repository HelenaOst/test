# ==================== CELERY НАЛАШТУВАННЯ ====================

CELERY_BROKER_URL = 'redis://redis:6379/0'           # Брокер повідомлень (Redis)
CELERY_RESULTS_BACKEND = 'django-db'                 # Зберігання результатів у БД
CELERY_ACCEPT_CONTENT = ['application/json']         # Формат даних
CELERY_TASK_SERIALIZER = 'json'                      # Серіалізація задач
CELERY_RESULT_SERIALIZER = 'json'                    # Серіалізація результатів