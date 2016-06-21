# Broker settings
BROKER_URL = 'redis://localhost:6379/'

# The backend used to store task results
CELERY_RESULT_BACKEND = 'redis://localhost:6379/'

# A whitelist of content-types/serializers to allow.
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
