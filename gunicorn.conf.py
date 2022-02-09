import os

worker_class = "uvicorn.workers.UvicornWorker"
workers = 3
accesslog = "-"
errorlog = "-"
bind = f"0.0.0.0:{os.getenv('HTTP_PORT')}"
