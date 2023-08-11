


class BaseConfig(object):
    pass



class DevConfig(BaseConfig):

    CELERY_BROKER_URL = "redis://:buzhidao@127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND = "redis://:buzhidao@127.0.0.1:6379/0"
