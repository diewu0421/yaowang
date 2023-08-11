# from celery_task.create_celery import celery_app
#
#
# @celery_app.task
# def send_mail():
#     # print(email, bug)
#     print('o2222222222k')
#     return 'success3232'
from celery_task import celery_app

print('tasks ', celery_app)

@celery_app.task
def send_mail(arg):
    print("send111111111111", arg)