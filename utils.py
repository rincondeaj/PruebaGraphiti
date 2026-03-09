#Probando
from datetime import datetime
from functools import wraps

def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[AUDIT] Executing {func.__name__} at {datetime.now()}")
        return func(*args, **kwargs)
    return wrapper

class AuditMixin:
    def __init__(self):
        self._audit_log: list[str] = []

    def add_audit_entry(self, action: str):
        entry = f"{datetime.now()}: {action}"
        self._audit_log.append(entry)
    
    @property
    def last_action(self) -> str:
        return self._audit_log[-1] if self._audit_log else "No actions"
