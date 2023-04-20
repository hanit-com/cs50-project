import sys


class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = "sqlite:///data/project.db"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = "sqlite:///data/test.db"


def get_config():
    is_testing = 'pytest' in sys.argv[0]
    if is_testing:
        return TestingConfig()
    else:
        return DevelopmentConfig()


config = get_config()