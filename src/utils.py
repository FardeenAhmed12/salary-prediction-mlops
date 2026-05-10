import os

def get_env_var(key, default=None):
    return os.getenv(key, default)

def setup_logging():
    import logging
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)