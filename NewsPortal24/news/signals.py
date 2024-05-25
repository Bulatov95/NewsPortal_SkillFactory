import os

from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from NewsPortal24 import settings
from news.models import Post, Subscriber


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":  # отправка уведомления только при добавлении категорий.
        # print(f"notify_subscribers вызвали публикацию id={instance.id}")
        if instance.id:
            print("Сообщение создано, отправка писем")
            categories = instance.category.all()
            if categories:
                for category in categories:
                    subscribers = Subscriber.objects.filter(category=category)
                    for subscriber in subscribers:
                        if subscriber.user.email:
                            print(f"Отправка электронной почты на {subscriber.user.email}")
                            send_mail(
                                'Новый пост в категории, на которую вы подписаны',
                                f'Посмотреть можно здесь: http://127.0.0.1:8000/News/{instance.id}',
                                f"{os.getenv('DEFAULT_FROM_EMAIL')}",
                                [subscriber.user.email],
                                )
                        else:
                            print(f"Нет электронной почты для пользователя {subscriber.user.username}")
            else:
                print("Нет категорий для этого сообщения")
        else:
            print("Пост не создан, письма не отправляются")