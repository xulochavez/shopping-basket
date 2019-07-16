class Config():
    DEBUG = True
    TESTING = False


class TestConfig(Config):
    DEBUG = True
    TESTING = True
