import threading


def run_in_thread(fn, daemon: bool = True):
    def run(*args, **kwargs):
        t = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=daemon)
        t.start()
        return t
    return run


def set_interval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():
                while not stopped.wait(interval):
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True
            t.start()
            return stopped
        return wrapper
    return decorator
