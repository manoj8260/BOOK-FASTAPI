from celery import Celery
from typing import List
from src.mails import create_message,mail
from asgiref.sync import async_to_sync

c_app = Celery("Recipe-Platform")
c_app.config_from_object('src.config')

@c_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_mail(self,recipients:List[str],subject :str,body : str) -> None:
   message = create_message(recipients=recipients,subject=subject,body=body)
   async_to_sync(mail.send_message)(message)

@c_app.task()
def add(x,y):
    return x+y   


