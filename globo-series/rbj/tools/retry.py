import time 
import logging 
from functools import wraps


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def warpper(*args, **kwargs):
            for attemps in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Attempt {attemps + 1} failed: {e}")
                    if attemps == max_attempts - 1:
                        raise e
                    else:
                        time.sleep(delay)
        return warpper
    return decorator 
