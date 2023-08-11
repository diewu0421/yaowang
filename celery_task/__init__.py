from celery import Celery

def make_celery():
    celery = Celery("default", backend="redis://:buzhidao@127.0.0.1:6379/0",
                    broker="redis://:buzhidao@127.0.0.1:6379/0" , include=['celery_task.tasks'])

    # celery.task(name="send_mail")(send_mail)
    return celery


celery_app = make_celery()

print("create_celerY", celery_app)

