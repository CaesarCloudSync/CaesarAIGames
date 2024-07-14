import os
import time

from celery import Celery
from CaesarAIGames.CaesarAIGames import CaesarAIGames

celery = Celery(__name__)
caesaraigames = CaesarAIGames()
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="create_task")
def create_task(url,filename):

    print(filename,"ham")
    caesaraigames.download(url,filename=f"/media/amari/SSD T7/steamunlockedgames/{filename}")
    return True