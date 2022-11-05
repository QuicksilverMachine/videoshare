"""
Gunicorn configuration for use in production.
"""
proc_name = "videoshare"
bind = ":8000"
workers = "1"
threads = "1"
timeout = 30
graceful_timeout = 30
max_requests = 100
max_requests_jitter = 50
