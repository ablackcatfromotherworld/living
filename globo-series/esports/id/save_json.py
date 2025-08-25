from functools import wraps
import json
from pathlib import Path
import inspect

def save_json(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            caller_file = inspect.getfile(func)
            caller_dir = Path(caller_file).parent
            with open(caller_dir / f'{name}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return data
        return wrapper
    return decorator