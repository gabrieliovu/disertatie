from celery import Celery
app = Celery()


@app.task(bind=True)
def send_message_check(self):
    print('Task did run')