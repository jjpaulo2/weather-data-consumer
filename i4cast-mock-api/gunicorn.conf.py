from multiprocessing import cpu_count
from i4cast_mock_api.dependencies import app_settings


bind = app_settings().host_binding()
workers = 2 * cpu_count() + 1
max_requests_jitter = 5
worker_class = 'uvicorn.workers.UvicornWorker'
max_requests = int(workers * 2000)
errorlog = '-'
timeout = 90
