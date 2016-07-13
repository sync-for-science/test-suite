""" Celery configuration.
"""
# Broker settings
BROKER_URL = 'redis://localhost:6379/'

# The backend used to store task results
CELERY_RESULT_BACKEND = 'redis://localhost:6379/'

# A whitelist of content-types/serializers to allow.
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Limit celery tasks so that if one hangs it doesn't lock the server forever
CELERYD_TASK_TIME_LIMIT = 15 * 60

# Restart every time in case of memory leaks
CELERYD_MAX_TASKS_PER_CHILD = 1

# We should be able to handle more than 2 task runners
CELERYD_CONCURRENCY = 4
