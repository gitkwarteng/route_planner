from main.settings.base import BASE_DIR

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'app.log',
            'formatter': 'json',
        },
        'client_file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'client.log',
            'formatter': 'json',
        },
        'route_file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'route.log',
            'formatter': 'json',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'routing': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'routing.client': {
            'handlers': ['console', 'client_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'routing.route': {
            'handlers': ['console', 'route_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}