# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from .models import PostCategory
# from django.core.mail import send_mail  # для простого письма
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def notify_subscribers(sender, instance, action, **kwargs):
#     if action:
#         subject = f'New post'
#         # отправка простого письма одному пользователю
#         send_mail(
#             subject=subject,  # тема письма - заголовок статьи
#             message=f'Test message about new post',  # сообщение в письме
#             from_email='a.v.lysenkov@yandex.ru',  # почта, с которой отправляется письмо
#             recipient_list=['a.v.lysenkov@gmail.com']  # список получателей
#         )
