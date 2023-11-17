from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy


@shared_task
def send_email(emails: list, todo):
    send_mail(
        subject='Uploaded new Todo',
        message=f'''
Title: {todo['title']}
Description: {todo['description']}
Price: {todo['price']}
Link: http://127.0.0.1:8000/api/todo-update/{todo['id']}
        ''',
        from_email='From P15Team',
        recipient_list=emails,
        fail_silently=True
    )
    return 'Done'
