from datetime import timedelta

SIMPLE_JWT = {
    # Час життя токенів
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # 1 година
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # 7 днів

    # Ротація токенів
    "ROTATE_REFRESH_TOKENS": True,  # Оновлювати refresh при використанні
    "BLACKLIST_AFTER_ROTATION": True,  # Додавати старі до чорного списку

    # Безпека та зручність
    "UPDATE_LAST_LOGIN": True,  # Оновлювати час останнього входу
    "AUTH_HEADER_TYPES": ("Bearer",),  # Тип токена в заголовку
}