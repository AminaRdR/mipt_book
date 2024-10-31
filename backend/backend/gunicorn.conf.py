from multiprocessing import cpu_count
from os import environ

# Настройки для Gunicorn

bind = '0.0.0.0:' + environ.get('PORT', '8000')  # Привязка к порту
max_requests = 1000  # Максимальное количество запросов на одного работника
worker_class = 'gevent'  # Использование gevent для асинхронной обработки
workers = 4  # Количество рабочих процессов - количество ядер CPU 2 + 1
reload = False  # Отключение перезагрузки при изменениях кода в production
name = 'backend'  # Имя приложения

# Дополнительные настройки

env = {
    'DJANGO_SETTINGS_MODULE': 'backend.settings' # Путь к вашим Django-настройкам
}

# Логирование

loglevel = 'info'
accesslog = '-'
errorlog = '-'

# Увеличение таймаута, чтобы не происходило прерывания долгоживущих запросов
timeout = 300

# Использование  HTTPS-протокола (если требуется)
secure_scheme = 'https'

# Установка прокси-заголовков для правильной обработки IP-адресов (если требуется)
for_x_forwarded_proto = 'https' 
