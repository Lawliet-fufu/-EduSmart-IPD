import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MySQL base config (can be overridden by DATABASE_URL / DEV_DATABASE_URL)
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'edusmart')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # Prefer explicit URL env vars when provided
        override_url = getattr(self, '_override_db_url', None)
        if override_url:
            return override_url
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

    def __init__(self):
        dev_url = os.environ.get('DEV_DATABASE_URL')
        if dev_url:
            self._override_db_url = dev_url

class ProductionConfig(Config):
    def __init__(self):
        prod_url = os.environ.get('DATABASE_URL')
        if prod_url:
            self._override_db_url = prod_url

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
