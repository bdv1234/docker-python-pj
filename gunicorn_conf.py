import multiprocessing
bind = "0.0.0.0:5002"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 30
accesslog = '-' # stdout
errorlog = '-'