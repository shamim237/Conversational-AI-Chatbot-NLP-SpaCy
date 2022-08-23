import os

class DefaultConfig:
    EXPIRE_AFTER_SECONDS = os.environ.get("ExpireAfterSeconds", 86400) 